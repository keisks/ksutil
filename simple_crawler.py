#!/usr/bin/env python3
"""
simple_crawler.py  –  resumable & polite version
-------------------------------------------------
Usage examples
--------------
# resume-capable HTML-only crawl, 0.5 s between requests
python simple_crawler.py https://texample.net --delay 0.5

# add JPGs, respect robots.txt, custom state file
python simple_crawler.py https://texample.net --ext jpg \
    --respect-robots --state texample.visited
"""
import argparse
import os
import queue
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib import robotparser

import requests
from bs4 import BeautifulSoup

###############################################################################
# Helper functions (unchanged except where noted)
###############################################################################

def same_origin(url_a: str, url_b: str) -> bool:
    a, b = urlparse(url_a), urlparse(url_b)
    return (a.scheme, a.netloc) == (b.scheme, b.netloc)

def local_path_for(url: str, mirror_root: Path) -> Path:
    parsed = urlparse(url)
    path = Path(parsed.path.lstrip("/"))
    if not path.suffix:
        path = path / "index.html"
    return mirror_root / path

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
          respect_robots: bool) -> None:

    # -------------------------------------------------------------------------
    # Load previously-visited URLs for resuming
    # -------------------------------------------------------------------------
    visited: set[str] = set()
    if state_file.exists():
        with open(state_file, "r", encoding="utf-8") as f:
            visited = {line.strip() for line in f if line.strip()}
        print(f"[resume] loaded {len(visited)} visited URLs from {state_file}")

    # -------------------------------------------------------------------------
    # Initialise queue (BFS frontier) and robots.txt if needed
    # -------------------------------------------------------------------------
    q: queue.Queue[str] = queue.Queue()
    q.put(start_url)
    rp = get_robotparser(start_url) if respect_robots else None
    user_agent_hdr = {"User-Agent": "SimpleCrawler"}

    # -------------------------------------------------------------------------
    # Crawl loop
    # -------------------------------------------------------------------------
    while not q.empty():
        url = q.get()

        # Skip if already seen
        if url in visited:
            continue

        # robots.txt check -----------------------------------------------------
        if rp and not allowed_by_robots(rp, url):
            print(f"[skip-robots] {url}")
            continue

        # Polite delay ---------------------------------------------------------
        if delay > 0:
            time.sleep(delay)

        # Fetch ---------------------------------------------------------------
        try:
            resp = requests.get(url, timeout=10, headers=user_agent_hdr)
            resp.raise_for_status()
        except Exception as exc:
            print(f"[warn] failed {url}: {exc}", file=sys.stderr)
            continue

        # Mark as visited *and* persist immediately
        visited.add(url)
        with open(state_file, "a", encoding="utf-8") as f:
            print(url, file=f)

        content_type = resp.headers.get("content-type", "")
        suffix = Path(urlparse(url).path).suffix.lower().lstrip(".")

        # ---------------------------------------------------------------------
        # Decide how to handle the fetched resource
        # ---------------------------------------------------------------------
        if "text/html" in content_type or suffix in {"", "html", "htm"}:
            dest = local_path_for(url, mirror_root)
            save_binary(resp.content, dest)
            print(f"[html]  {url}  ->  {dest.relative_to(mirror_root)}")

            soup = BeautifulSoup(resp.content, "html.parser")

            # enqueue hyperlinks
            for link in soup.find_all("a", href=True):
                abs_href = urljoin(url, link["href"])
                if same_origin(start_url, abs_href) and urlparse(abs_href).scheme in {"http", "https"}:
                    q.put(abs_href)

            # enqueue common asset tags (img, script, css)
            asset_tags = (
                soup.find_all("img", src=True)
                + soup.find_all("script", src=True)
                + soup.find_all("link", href=True)
            )
            for tag in asset_tags:
                attr = "src" if tag.has_attr("src") else "href"
                abs_ref = urljoin(url, tag[attr])
                if same_origin(start_url, abs_ref):
                    q.put(abs_ref)

        elif suffix in wanted_exts:
            dest = local_path_for(url, mirror_root)
            save_binary(resp.content, dest)
            print(f"[file] {url}  ->  {dest.relative_to(mirror_root)}")

        # (other content types silently ignored)

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
    args = parser.parse_args()

    start_url = args.start_url.rstrip("/") + "/"
    wanted_exts = {e.lower().lstrip(".") for e in args.ext}
    mirror_root = Path(args.out).resolve()
    state_file = Path(args.state).resolve()

    print(f"Start URL     : {start_url}")
    print(f"Mirror dir    : {mirror_root}")
    print(f"Visited state : {state_file}")
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
          args.respect_robots)

if __name__ == "__main__":
    main()
