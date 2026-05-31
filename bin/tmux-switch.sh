#!/usr/bin/env bash

session="$(tmux list-sessions -F '#S' | fzf --prompt='tmux session> ')" || exit 1
[ -n "$session" ] && tmux switch-client -t "$session"
