#!/bin/sh

[ -z "$1" ] && ct=esvk2pod || ct="$1"

cd `dirname "$0"`

./remove-ct.sh "$ct"
./remove-image.sh "$ct"

