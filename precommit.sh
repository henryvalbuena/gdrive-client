#!/bin/bash

# Created a Symbolic link to this script with the following command
# ln -s ~/Docs/Projects/Python/gdrive/precommit.sh ~/Docs/Projects/Python/gdrive/gdrive_venv/bin/precommit 
# Any changes, please update

# Commit function
commit() {
    if [ "$1" == "-a" ]; then
        git add -A&&git commit --amend
    else
        git add -A&&git commit -m "$1"
    fi
    if [ "$?" -eq 0 ]
    then
        echo $'\nPre-commit script done!'
    fi
}

# Capturing flake8 
flake() {
    flake8
    if [ "$?" -gt 0 ]
    then
        echo $'\n* * * W A R N I N G * * *\n'
        echo $'Check flake8 errors before committing to branch\n'
        return 1
    fi
}

# Command chain
pytest -v&&flake&&commit "$1"