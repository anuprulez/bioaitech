#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 build.py
test -f dist/index.html
test -f dist/CNAME
test -f dist/sitemap.xml
echo "Build checks passed."
