#!/bin/sh

PORT=8080
[ -n "$2" ] && PORT="$2"

docker build -t esvk2pod . 
[ -z "$1" ] && docker run -d --name esvk2pod -p $PORT:8080 esvk2pod || docker run -d --name esvk2pod -e URLPREF="$1" -p $PORT:8080 esvk2pod

