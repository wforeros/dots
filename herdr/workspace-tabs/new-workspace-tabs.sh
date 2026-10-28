#!/usr/bin/env bash
# Renames the tab that comes with a new workspace to "Agents" and adds two more.
# Triggered by the workspace.created plugin event; the event JSON carries the id.
set -euo pipefail

herdr="${HERDR_BIN_PATH:-herdr}"
ws=$(printf '%s' "${HERDR_PLUGIN_EVENT_JSON:-}" \
  | jq -r '.data.workspace.workspace_id // .workspace.workspace_id // .workspace_id // empty')

[ -n "$ws" ] || exit 0

# The workspace already owns one tab: reuse it instead of adding a fourth.
first=$(printf '%s' "$("$herdr" tab list --workspace "$ws")" | jq -r '.result.tabs[0].tab_id // empty')

if [ -n "$first" ]; then
  "$herdr" tab rename "$first" "Agents" >/dev/null
else
  "$herdr" tab create --workspace "$ws" --label "Agents" --no-focus >/dev/null
fi

# Pin the new tabs to the workspace directory: without --cwd they follow the
# terminal.new_cwd policy, which can point somewhere else than the workspace.
dir=$(printf '%s' "$("$herdr" pane list --workspace "$ws")" | jq -r '.result.panes[0].cwd // empty')
cwd=()
[ -n "$dir" ] && cwd=(--cwd "$dir")

"$herdr" tab create --workspace "$ws" "${cwd[@]}" --label "Code" --no-focus >/dev/null
"$herdr" tab create --workspace "$ws" "${cwd[@]}" --label "Commands" --no-focus >/dev/null
