#!/usr/bin/env bash
# Render every docs/diagrams/src/*.mmd to PNG + PDF, then build docs/diagrams/diagram-book.pdf.
# Usage: bash tools/render_diagrams.sh
# First run downloads Mermaid CLI + headless Chromium via npx (one time, ~150–200 MB).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
D="$ROOT/docs/diagrams"
MMDC=(npx -y -p @mermaid-js/mermaid-cli@11.4.2 mmdc)
CFG="$D/src/_config.json"
mkdir -p "$D/png" "$D/pdf"
shopt -s nullglob
for src in "$D"/src/*.mmd; do
  name="$(basename "$src" .mmd)"
  echo "render $name"
  "${MMDC[@]}" -q -i "$src" -o "$D/png/$name.png" -c "$CFG" -b white -s 3 -w 1600
  "${MMDC[@]}" -q -i "$src" -o "$D/pdf/$name.pdf" -c "$CFG" -b white -f
done
pdfs=("$D"/pdf/*.pdf)
if command -v pdfunite >/dev/null && ((${#pdfs[@]})); then
  pdfunite "${pdfs[@]}" "$D/diagram-book.pdf"
  echo "book -> docs/diagrams/diagram-book.pdf (${#pdfs[@]} diagrams)"
fi
