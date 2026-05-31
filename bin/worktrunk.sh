#!/usr/bin/env bash

# Worktrunk create
wtc() {
  local origin="$PWD"
  local branch="$1"
  local base="${2:-@}"
  wt switch --create "$branch" --base "$base"
  cd "$origin"
}

wts() {
  local worktree = $(wt list --format json | jq -r -S ".[].branch" | sort | fzf --prompt "switch worktree > ")
  "wt switch $worktree"
}

# wtr() {
#   local worktree = $(wt list --format json | jq -r -S ".[].branch" | sort | fzf --prompt "remove worktree > ")
#   echo "Worktree to remove: $worktree"
#   if [ ! "wt remove $worktree" ]; then
#     echo "Error while trying to remove the worktree"
#   fi
# }
