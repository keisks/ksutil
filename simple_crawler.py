#!/usr/bin/env python3
"""
simple_crawler.py  –  resumable & polite version
-------------------------------------------------
Usage examples
--------------
# resume-capable HTML-only crawl, 0.5 s between requests
python simple_crawler.py https://example.net --delay 0.5

# add JPGs, respect robots.txt, custom state file
python simple_crawler.py https://example.net --ext jpg \
    --respect-robots --state example.visited
"""
import argparse
import os
import queue
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse
from urllib import robotparser

import requests
from bs4 import BeautifulSoup

###############################################################################
# Helper functions
###############################################################################

def normalize_url(url: str) -> str:
    """Normalize URL to avoid visiting duplicates"""
    parsed = urlparse(url)
    # Remove fragment
    parsed = parsed._replace(fragment='')
    # Remove trailing slash from path (except for root)
    if parsed.path.endswith('/') and parsed.path != '/':
        parsed = parsed._replace(path=parsed.path.rstrip('/'))
    # Remove default ports
    netloc = parsed.netloc
    if (parsed.scheme == 'http' and netloc.endswith(':80')) or \
       (parsed.scheme == 'https' and netloc.endswith(':443')):
        netloc = netloc.rsplit(':', 1)[0]
        parsed = parsed._replace(netloc=netloc)
    return urlunparse(parsed)

def same_origin(url_a: str, url_b: str) -> bool:
    a, b = urlparse(url_a), urlparse(url_b)
    return (a.scheme, a.netloc) == (b.scheme, b.netloc)

def local_path_for(url: str, mirror_root: Path) -> Path:
    """Convert URL to local filesystem path (with security checks)"""
    parsed = urlparse(url)
    path = parsed.path.lstrip("/")
    
    # Security: sanitize path components
    safe_parts = []
    for part in Path(path).parts:
        # Skip dangerous patterns
        if part in {'.', '..'} or part.startswith('.'):
            continue
        # Basic sanitization
        safe_part = "".join(c for c in part if c.isalnum() or c in '-_.')
        if safe_part:
            safe_parts.append(safe_part)
    
    path = Path(*safe_parts) if safe_parts else Path("index")
    
    if not path.suffix:
        path = path / "index.html"
    
    # Ensure we stay within mirror_root
    full_path = (mirror_root / path).resolve()
    if not str(full_path).startswith(str(mirror_root.resolve())):
        raise ValueError(f"Path escape attempt: {url}")
    
    return full_path

def save_binary(content: bytes, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "wb") as f:
        f.write(content)

###############################################################################
# Politeness helpers
###############################################################################

def get_robotparser(origin: str, user_agent: str = "SimpleCrawler") -> robotparser.RobotFileParser:
    rp = robotparser.RobotFileParser()
    rp.set_url(urljoin(origin, "/robots.txt"))
    try:
        rp.read()
    except Exception:
        # If robots.txt cannot be fetched, fall back to "allow all"
        rp = None
    return rp

def allowed_by_robots(rp, url: str, user_agent: str = "SimpleCrawler") -> bool:
    if rp is None:
        return True
    return rp.can_fetch(user_agent, url)

###############################################################################
# Main crawler
###############################################################################

def crawl(start_url: str,
          wanted_exts: set[str],
          mirror_root: Path,
          state_file: Path,
          delay: float,
          respect_robots: bool,
          max_pages: int = 10000,
          max_file_size: int = 100*1024*1024) -> None:

    # -------------------------------------------------------------------------
    # Load previously-visited URLs for resuming
    # -------------------------------------------------------------------------
    visited: set[str] = set()
    reseed_urls: list[str] = []  # URLs to re-parse for finding new links
    
    if state_file.exists():
        with open(state_file, "r", encoding="utf-8") as f:
            all_visited = [line.strip() for line in f if line.strip()]
            visited = set(all_visited)

        print(f"[resume] loaded {len(visited)} visited URLs from {state_file}")
        
        # On resume, we need to re-parse some HTML pages to find unvisited links
        # Take the last 20 HTML pages we visited
        for url in reversed(all_visited[-20:]):
            parsed_url = urlparse(url)
            suffix = Path(parsed_url.path).suffix.lower().lstrip(".")
            if suffix in {"", "html", "htm"}:
                reseed_urls.append(url)
    
    pages_crawled = len(visited)

    # -------------------------------------------------------------------------
    # Initialise queue (BFS frontier) and robots.txt if needed
    # -------------------------------------------------------------------------
    q: queue.Queue[str] = queue.Queue()
    q.put(normalize_url(start_url))
    rp = get_robotparser(start_url) if respect_robots else None
    
    session = requests.Session()
    session.headers.update({"User-Agent": "SimpleCrawler"})
    
    # -------------------------------------------------------------------------
    # Re-seed queue by re-parsing recent HTML pages (resume mode)
    # -------------------------------------------------------------------------
    if reseed_urls:
        print(f"[resume] re-parsing {len(reseed_urls)} recent HTML pages to find new links...")
        for url in reseed_urls:
            try:
                local_file = local_path_for(url, mirror_root)
                if local_file.exists():
                    with open(local_file, "rb") as f:
                        content = f.read()
                    soup = BeautifulSoup(content, "html.parser")
                    
                    # Re-discover links
                    for link in soup.find_all("a", href=True):
                        abs_href = urljoin(url, link["href"])
                        normalized = normalize_url(abs_href)
                        if same_origin(start_url, abs_href) and \
                           urlparse(abs_href).scheme in {"http", "https"} and \
                           normalized not in visited:
                            q.put(abs_href)
                    
                    # Re-discover assets
                    asset_tags = (
                        soup.find_all("img", src=True)
                        + soup.find_all("script", src=True)
                        + soup.find_all("link", href=True, rel=lambda x: x and "stylesheet" in x)
                    )
                    for tag in asset_tags:
                        attr = "src" if tag.has_attr("src") else "href"
                        abs_ref = urljoin(url, tag[attr])
                        normalized = normalize_url(abs_ref)
                        if same_origin(start_url, abs_ref) and normalized not in visited:
                            q.put(abs_ref)
            except Exception as e:
                # If we can't re-parse, skip silently
                pass
        
        print(f"[resume] found {q.qsize()} unvisited URLs to explore")

    # -------------------------------------------------------------------------
    # Crawl loop
    # -------------------------------------------------------------------------
    while not q.empty():
        # Check page limit
        if pages_crawled >= max_pages:
            print(f"[limit] Reached maximum pages ({max_pages})")
            break
            
        url = q.get()
        normalized_url = normalize_url(url)

        # Skip if already seen (check normalized version)
        if normalized_url in visited:
            continue

        # robots.txt check -----------------------------------------------------
        if rp and not allowed_by_robots(rp, normalized_url):
            print(f"[skip-robots] {normalized_url}")
            continue

        # Polite delay ---------------------------------------------------------
        if delay > 0:
            time.sleep(delay)

        # Fetch ---------------------------------------------------------------
        try:
            resp = session.get(normalized_url, timeout=10, allow_redirects=True)
            resp.raise_for_status()
            
            # Check file size
            if len(resp.content) > max_file_size:
                print(f"[skip-size] {normalized_url} ({len(resp.content)} bytes)")
                continue
                
        except Exception as exc:
            print(f"[warn] failed {normalized_url}: {exc}", file=sys.stderr)
            continue

        # Mark as visited *and* persist immediately
        visited.add(normalized_url)
        pages_crawled += 1
        with open(state_file, "a", encoding="utf-8") as f:
            print(normalized_url, file=f)

        content_type = resp.headers.get("content-type", "")
        suffix = Path(urlparse(normalized_url).path).suffix.lower().lstrip(".")

        # ---------------------------------------------------------------------
        # Decide how to handle the fetched resource
        # ---------------------------------------------------------------------
        if "text/html" in content_type or suffix in {"", "html", "htm"}:
            try:
                dest = local_path_for(normalized_url, mirror_root)
                save_binary(resp.content, dest)
                print(f"[html]  {normalized_url}  ->  {dest.relative_to(mirror_root)}")
            except ValueError as e:
                print(f"[skip-security] {normalized_url}: {e}", file=sys.stderr)
                continue

            soup = BeautifulSoup(resp.content, "html.parser")

            # enqueue hyperlinks
            for link in soup.find_all("a", href=True):
                abs_href = urljoin(normalized_url, link["href"])
                if same_origin(start_url, abs_href) and urlparse(abs_href).scheme in {"http", "https"}:
                    q.put(abs_href)

            # enqueue common asset tags (img, script, css)
            asset_tags = (
                soup.find_all("img", src=True)
                + soup.find_all("script", src=True)
                + soup.find_all("link", href=True, rel=lambda x: x and "stylesheet" in x)
            )
            for tag in asset_tags:
                attr = "src" if tag.has_attr("src") else "href"
                abs_ref = urljoin(normalized_url, tag[attr])
                if same_origin(start_url, abs_ref):
                    q.put(abs_ref)

        elif suffix in wanted_exts:
            try:
                dest = local_path_for(normalized_url, mirror_root)
                save_binary(resp.content, dest)
                print(f"[file] {normalized_url}  ->  {dest.relative_to(mirror_root)}")
            except ValueError as e:
                print(f"[skip-security] {normalized_url}: {e}", file=sys.stderr)
                continue

        # (other content types silently ignored)

    print(f"\n[done] Crawled {pages_crawled} pages")

###############################################################################
# Entry point
###############################################################################

def main():
    parser = argparse.ArgumentParser(description="Tiny resumable single-origin web crawler")
    parser.add_argument("start_url", help="e.g. https://example.com")
    parser.add_argument("--ext", nargs="*", default=[], help="Extra extensions to download")
    parser.add_argument("--out", default="mirror", help="Directory for mirrored site")
    parser.add_argument("--state", default="visited.txt", help="File to store visited URLs")
    parser.add_argument("--delay", type=float, default=5.0,
                        help="Seconds to wait between requests (politeness)")
    parser.add_argument("--respect-robots", action="store_true",
                        help="Respect robots.txt (skips disallowed URLs)")
    parser.add_argument("--max-pages", type=int, default=10000,
                        help="Maximum number of pages to crawl")
    parser.add_argument("--max-file-size", type=int, default=100*1024*1024,
                        help="Maximum file size in bytes (default: 100MB)")
    args = parser.parse_args()

    start_url = args.start_url.rstrip("/")
    if not start_url.endswith('/') and not Path(urlparse(start_url).path).suffix:
        start_url += "/"
    
    wanted_exts = {e.lower().lstrip(".") for e in args.ext}
    mirror_root = Path(args.out).resolve()
    state_file = Path(args.state).resolve()

    print(f"Start URL     : {start_url}")
    print(f"Mirror dir    : {mirror_root}")
    print(f"Visited state : {state_file}")
    print(f"Max pages     : {args.max_pages}")
    print(f"Max file size : {args.max_file_size / (1024*1024):.1f} MB")
    if wanted_exts:
        print(f"Extra types   : {', '.join(sorted(wanted_exts))}")
    if args.delay:
        print(f"Request delay : {args.delay:.2f} s")
    if args.respect_robots:
        print("Robots.txt    : respected")

    crawl(start_url,
          wanted_exts,
          mirror_root,
          state_file,
          args.delay,
          args.respect_robots,
          args.max_pages,
          args.max_file_size)

if __name__ == "__main__":
    main()
