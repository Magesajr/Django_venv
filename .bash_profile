if [ -f ~/.bashrc ]; then
    source ~/.bashrc

fi

alias c='clear'

alias DBstart='pg_ctl -D ./postgres start'
alias DBstop='pg_ctl -D ./postgres start'

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
if command -v pyenv 1>/dev/null 2>&1; then
 eval "$(pyenv init -)"
fi
. "$HOME/.cargo/env"
