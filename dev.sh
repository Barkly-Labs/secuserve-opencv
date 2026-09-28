#!/bin/bash

PS1=$
PROMPT_COMMAND=
echo -en "\033]0;Opencv Backend\a"

echo "setting env vars"
source  /home/nicky/.cache/pypoetry/virtualenvs/secuserve-module-opencv-_X9nZv5C-py3.8/bin/activate

poetry run python3 SecuServe-Module-opencv/