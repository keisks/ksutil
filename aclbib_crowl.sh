#!/bin/sh

# tiny script for crowling acl-anthology and create acl_all.bib.
wget -w 1 --user-agent="Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)" -r -N -np -A .bib http://aclweb.org/anthology-new/
find . -name "*.bib" |xargs -i% cat % > acl_all.bib
