#!/bin/sh

[ -z "$1" ] && ct=esvk2pod || ct="$1"

echo "Stopping container $1..."
docker stop $ct
echo "Removing container..."
docker rm $ct

#echo "Removing image..."
#docker rmi $ct

