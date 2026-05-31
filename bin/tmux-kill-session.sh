#!/usr/bin/env bash

session=$(tmux ls | fzf --prompt='tmux kill session> ' | sed "s/:.*//")
[ -n "$session" ] && tmux kill-session -t $session
