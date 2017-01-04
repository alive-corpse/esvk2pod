#!/bin/sh

[ -z "$1" ] && ct=esvk2pod || ct="$1"

echo "Removing image..."
docker rmi $ct

