#!/usr/bin/bash

# check if by default generate error
if ./isUpdated.sh  > /dev/null 2>&1; then
    echo expected error by default
    exit
else
    echo -n "."
fi

export AUTO_GIT_SYNC_BRANCH=test


# check if get the env variable
if ! ./isUpdated.sh  > /dev/null 2>&1; then
    echo no error expected
    exit
else
    echo -n "."
fi

echo
echo OK