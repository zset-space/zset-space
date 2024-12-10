#!/usr/bin/env bash

set -euo pipefail

say() { echo -e "\e[1;32m$@\e[0m"; } >&2
err() { echo -e "\e[1;31m$@\e[0m"; } >&2

for title in "$@"; do
    printf -v url 'https://en.wikipedia.org/w/index.php?action=raw&title=%s' "$title"
    printf "\n<!-- START %s -->\n" "$url"
    say "GET $url" && curl -s "$url"
    printf "\n<!-- END %s -->\n" "$url"
done