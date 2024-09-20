#!/bin/sh
export XDG_CONFIG_HOME="$HOME"/.config
os=$(uname)
echo "OS: $os"
mkdir -p "$XDG_CONFIG_HOME"

ln -s "$PWD/nvim" "$XDG_CONFIG_HOME/nvim"

ln -s "$PWD/.zshrc" "$HOME/.zshrc"
ln -s "$PWD/.tmux.conf" "$HOME/.tmux.conf"
ln -s "$PWD/.gitconfig" "$HOME/.gitconfig"

if [ "$os" = "Darwin" ]; then
	echo "Setting up MacOS"
	brew install zsh
	brew install neovim
	brew install tmux
elif [ "$os" = "Linnux" ]; then
	echo "Setting up Linux"
	sudo apt install zsh
	sudo apt install tmux
	sudo apt install neovim
fi
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
