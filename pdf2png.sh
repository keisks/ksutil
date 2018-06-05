#!/bin/sh
# imagemagick is required.

for f in $(ls *.pdf) 
do
  f2=`echo $f | sed -e "s/pdf$/png/"` 
  convert $f $f2 
done
