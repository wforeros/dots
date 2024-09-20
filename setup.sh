#!/bin/sh
export XDG_CONFIG_HOME="$HOME"/.config
os=$(uname)
echo "OS: $os"
mkdir -p "$XDG_CONFIG_HOME"

if [ "$os" = "Darwin" ]; then
	echo "Setting up MacOS"
	brew install zsh
	brew install neovim
	brew install tmux
elif [ "$os" = "Linux" ]; then
	echo "Setting up Linux"
	sudo apt install zsh
	sudo apt install tmux
	sudo apt install neovim
fi
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

ln -s "$PWD/.zshrc" "$HOME/.zshrc"
ln -s "$PWD/tmux/tmux.conf" "$HOME/.tmux.conf"
ln -s "$PWD/.gitconfig" "$HOME/.gitconfig"
