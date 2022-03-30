#!/bin/bash

last_rebase_hash=$(git reflog --grep-reflog="rebase" --pretty=format:"%h" -n 1)
last_commit_hash=$(git rev-parse --verify HEAD)
commits_after_rebase=$(git log $last_rebase_hash..$last_commit_hash --pretty=oneline | wc -l)


if [ "$last_rebase_hash" = "" ]
then
python2 ./scrypt.py
GIT_SEQUENCE_EDITOR='cat ./git-script/git_rebase_file >' git rebase -i --keep-empty --root master

else
if [ "$commits_after_rebase" \> 20 ]
then
python2 ./scrypt.py -n $commits_after_rebase
GIT_SEQUENCE_EDITOR='cat ./git-script/git_rebase_file >' git rebase -i --keep-empty HEAD~$commits_after_rebase master
fi

fi

rm ./git_rebase_file