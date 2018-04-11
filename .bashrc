#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return
tmux_mgr () {
  if [[ ${TERM} != tmux ]]
  then
    if [[ $( tmux list-sessions ) ]]
    then
      tmux list-sessions
      read -p "Taper le numéro de session [0] : " sessionId
    fi
    sessionId=${sessionId:=0}
    [[ ${sessionId} =~ ^[0-9][0-9]*$ ]] && ( logger "Attachement à la session tmux ${sessionId}" ; tmux attach-session -t ${sessionId} ) || ( logger "Création d'une nouvelle session tmux" ; tmux )
  fi
}
get_rfc () {
  curl https://www.rfc-editor.org/rfc/rfc${1}.txt 2>/dev/null | sed -e "s/^.*$//g" \
        -e "s/^RFC ${i}.*$//" \
        -e "s/^.*\[Page [0-9]\+\]$//" | grep -vE "^\s*$" > rfc_${1}.txt
}


alias ls='ls --color=auto'
export HISTCONTROL=ignoreboth
export HISTIGNORE='ls:bg:fg:history'
export HISTSIZE=5000
export HISTFILESIZE=10000

export PATH=${PATH}:/home/yapoc/tools4work

export PS1='[\D{%H:%M:%S} - \u@\h \W]\$ '
export http_proxy="http://redacted"
export http_proxy="http://redacted"
export https_proxy="${http_proxy}"
export HTTP_PROXY="${http_proxy}"
export HTTPS_PROXY="${http_proxy}"
export no_proxy="localhost"
export VISUAL="vim"
export EDITOR="vim"
tmux_mgr
