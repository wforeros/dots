# Amazon Q pre block. Keep at the top of this file.
[[ -f "${HOME}/Library/Application Support/amazon-q/shell/zshrc.pre.zsh" ]] && builtin source "${HOME}/Library/Application Support/amazon-q/shell/zshrc.pre.zsh"
# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# Q pre block. Keep at the top of this file.
# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
export ZSH="$HOME/.oh-my-zsh"
ZSHRC_DIR="${0:A:h}"

# Set name of the theme to load --- if set to "random", it will
# load a random theme each time oh-my-zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
ZSH_THEME="powerlevel10k/powerlevel10k"

# Set list of themes to pick from when loading at random
# Setting this variable when ZSH_THEME=random will cause zsh to load
# a theme from this variable instead of looking in $ZSH/themes/
# If set to an empty array, this variable will have no effect.
# ZSH_THEME_RANDOM_CANDIDATES=( "robbyrussell" "agnoster" )

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion.
# Case-sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment one of the following lines to change the auto-update behavior
# zstyle ':omz:update' mode disabled  # disable automatic updates
# zstyle ':omz:update' mode auto      # update automatically without asking
# zstyle ':omz:update' mode reminder  # just remind me to update when it's time

# Uncomment the following line to change how often to auto-update (in days).
# zstyle ':omz:update' frequency 13

# Uncomment the following line if pasting URLs and other text is messed up.
# DISABLE_MAGIC_FUNCTIONS="true"

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# You can also set it to another string to have that shown instead of the default red dots.
# e.g. COMPLETION_WAITING_DOTS="%F{yellow}waiting...%f"
# Caution: this setting can cause issues with multiline prompts in zsh < 5.7.1 (see #5765)
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# You can set one of the optional three formats:
# "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# or set a custom format using the strftime function format specifications,
# see 'man strftime' for details.
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load?
# Standard plugins can be found in $ZSH/plugins/
# Custom plugins may be added to $ZSH_CUSTOM/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(git z zsh-syntax-highlighting)

source $ZSH/oh-my-zsh.sh

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

export CONFIG_DIR="$HOME/.config"

export PATH="$HOME/.config/bin:$PATH"
export PATH="$PATH:$HOME/squashfs-root/usr/bin"
# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run alias.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"# The next line updates PATH for the Google Cloud SDK.


# export PYENV_ROOT="$HOME/.pyenv"
# [[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
# eval "$(pyenv init -)"

# To customize prompt, run p10k configure or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
# alias ls='colorls'

alias ll='ls -l'
alias la='ls -a'
alias lla='ls -la'

alias c='clear'

export PATH="/home/linuxbrew/.linuxbrew/bin:$PATH"

# Cargar los scripts de fzf (key bindings y autocompletado)
for FZF_DIR in /opt/homebrew/opt/fzf /usr/local/opt/fzf /home/linuxbrew/.linuxbrew/opt/fzf "$HOME/.fzf"; do
  if [[ -f "$FZF_DIR/shell/key-bindings.zsh" ]]; then
    source "$FZF_DIR/shell/key-bindings.zsh"
    [[ -f "$FZF_DIR/shell/completion.zsh" ]] && source "$FZF_DIR/shell/completion.zsh"
    break
  fi
done
unset FZF_DIR

export FZF_DEFAULT_OPTS='--layout=reverse --border'
alias vf='nvim $(fzf --preview "bat --color=always {}")'

# Tmux
alias t="tmux"
alias tn="tmux new"
alias tls="tmux ls"
alias ta='tmux attach -t "$(tmux ls | fzf | sed  "s/:.*//")"'
# alias ts='~/dots/personal/dots/bin/tmux-sessionizer'
# alias tt='~/dots/personal/dots/bin/tmux-templates'
alias ts='~/dots/bin/tmux-sessionizer'
alias tt='~/dots/bin/tmux-template'
alias tks='tmux kill-session -t "$(tmux ls | fzf | sed  "s/:.*//")"'

# Git
alias lg="lazygit"
# source "$HOME/dots/personal/dots/bin/worktree"

alias lzd="lazydocker"

# Otros
mkcd() {
    mkdir -p "$1" && cd "$1"
}

# Amazon Q post block. Keep at the bottom of this file.
[[ -f "${HOME}/Library/Application Support/amazon-q/shell/zshrc.post.zsh" ]] && builtin source "${HOME}/Library/Application Support/amazon-q/shell/zshrc.post.zsh"


# . $HOME/.linuxbrew/opt/asdf/libexec/asdf.sh
# . $HOME/.linuxbrew/opt/asdf/etc/bash_completion.d/asdf.bash
if [[ -r /opt/homebrew/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]]; then
  source /opt/homebrew/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
fi
eval "$(fnm env --use-on-cd --shell zsh)"

# Refresh snap credentials
sc() {
  snapaccess credentials refresh --forceRefresh --email wforerosierra@c.snap.com
}

# Python
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
lazy_load_pyenv() {
  unset -f pyenv python python3 pip pip3 lazy_load_pyenv
  eval "$(pyenv init - zsh)"
}

pyenv() {
  lazy_load_pyenv
  pyenv "$@"
}

python() {
  lazy_load_pyenv
  python "$@"
}

python3() {
  lazy_load_pyenv
  python3 "$@"
}

pip() {
  lazy_load_pyenv
  pip "$@"
}

pip3() {
  lazy_load_pyenv
  pip3 "$@"
}

# The next line updates PATH for the Google Cloud SDK.
if [ -f '/Users/wforerosierra/google-cloud-sdk/path.zsh.inc' ]; then . '/Users/wforerosierra/google-cloud-sdk/path.zsh.inc'; fi

# The next line enables shell command completion for gcloud.
if [ -f '/Users/wforerosierra/google-cloud-sdk/completion.zsh.inc' ]; then . '/Users/wforerosierra/google-cloud-sdk/completion.zsh.inc'; fi

export PATH="/usr/local/bin:$PATH"

#THIS MUST BE AT THE END OF THE FILE FOR SDKMAN TO WORK!!!
export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"

# export DB_USER=postgres
# export DOCKER_DB=db
# export MY_USER_ID=testing@snapchat.com
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
lazy_load_nvm() {
  unset -f nvm node npm npx lazy_load_nvm
  [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
}

nvm() {
  lazy_load_nvm
  nvm "$@"
}

node() {
  lazy_load_nvm
  node "$@"
}

npm() {
  lazy_load_nvm
  npm "$@"
}

npx() {
  lazy_load_nvm
  npx "$@"
}

export PATH="$HOME/.local/bin:$PATH"
export EDITOR="nvim"

# Keep Ctrl+R mapped to fzf history after all startup scripts.
if (( $+functions[fzf-history-widget] )); then
  bindkey -M emacs '^R' fzf-history-widget
  bindkey -M viins '^R' fzf-history-widget
fi
