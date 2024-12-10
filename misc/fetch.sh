#!/usr/bin/env bash

set -euo pipefail

: ${URL=https://en.wikipedia.org/w/index.php?action=raw&title=}

say() { echo -e "\e[1;32m$@\e[0m"; } >&2
err() { echo -e "\e[1;31m$@\e[0m"; } >&2
sep() { echo -e "\n<!-- $1 $2 -->"; }
get() { curl -s "$URL$1" | sed -r '/^ *== *(Notes|References|Citations) *== *$/,/\Z/d'; }

for title in "$@"; do
    say "GET $title"
    sep "$title" start
    get "$title" || err "$title"
    sep "$title" done
done
