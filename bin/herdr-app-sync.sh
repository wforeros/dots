#!/usr/bin/env bash
# Deploy the Herdr app config kept in this repo to the Windows app folder.
# The repo is the source of truth; Herdr's own shipped mods/layouts (named in
# installed.json) are never touched.
#
#   herdr-app-sync.sh           repo -> C:\Users\PC\.config\herdr-app
#   herdr-app-sync.sh --pull    back, for changes made in the app's settings UI
#
# HERDR_APP_WIN overrides the Windows folder. Lives in ~/dots/bin.
set -euo pipefail

DOTS="${HERDR_APP_DOTS:-$HOME/dots/herdr/app}"
WIN="${HERDR_APP_WIN:-/mnt/c/Users/PC/.config/herdr-app}"
src=$DOTS dst=$WIN label="repo -> app"
if [ "${1:-}" = "--pull" ]; then src=$WIN dst=$DOTS label="app -> repo"; fi

shipped=$(jq -r 'keys[] | sub("^layout:"; "")' "$WIN/installed.json")

# Only what the person writes; Herdr's own state (view, shared, installed...) stays put.
list() {
  cd "$1"
  for f in settings.json keys.json; do [ -f "$f" ] && echo "$f"; done
  find layouts mods themes -maxdepth 3 -type f \
    ! -name 'jsconfig.json' ! -name '*.d.ts' ! -name '*.error' \
    ! -name '*.svg' ! -name '*.md' 2>/dev/null
}

changed=0
while IFS= read -r rel; do
  case "$rel" in
    layouts/*.json) name=${rel#layouts/}; name=${name%.json} ;;
    mods/*/*)       name=${rel#mods/}; name=${name%%/*} ;;
    *)              name="" ;;
  esac
  [ -n "$name" ] && printf '%s\n' "$shipped" | grep -qxF "$name" && continue
  cmp -s "$src/$rel" "$dst/$rel" 2>/dev/null && continue
  mkdir -p "$dst/$(dirname "$rel")"
  cp "$src/$rel" "$dst/$rel"
  echo "$label: $rel"
  changed=$((changed + 1))
done < <(list "$src" | sort)

echo "$changed file(s) synced ($label)"
