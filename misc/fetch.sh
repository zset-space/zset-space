#!/usr/bin/env bash

set -euo pipefail

: ${URL=https://en.wikipedia.org/w/index.php?action=raw&title=}

say() { echo -e "\e[1;32m$@\e[0m"; } >&2
err() { echo -e "\e[1;31m$@\e[0m"; } >&2
sep() { echo -e "\n<!-- $* -->"; }
get() {
    say GET "$1"
    sep START "$1"
    curl "$URL$1" \
        | sed -r '/^ *== *(Notes|References|Citations) *== *$/,$d' \
        | pandoc -f mediawiki -t gfm --wrap=preserve \
        || err "$title"
    sep DONE "$1"
}

for title in "$@"; do
    get "$title"
done
