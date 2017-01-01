#!/bin/sh

docker build -t esvk2pod . 
[ -z "$1" ] && docker run -d --name esvk2pod -p 8080:8080 esvk2pod || docker run -d --name esvk2pod -e URLPREF="$1" -p 8080:8080 esvk2pod

