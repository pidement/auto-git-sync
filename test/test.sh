#!/usr/bin/bash

# avoid use the default environment variable on this test file
export AUTO_GIT_SYNC_BRANCH=

# check if by default generate error
if ./isUpdated.sh  > /dev/null 2>&1; then
    echo expected error by default
    exit 1
else
    echo -n "."
fi

export AUTO_GIT_SYNC_BRANCH=test


# check if get the env variable
if ! ./isUpdated.sh  > /dev/null 2>&1; then
    echo no error expected
    exit 1
else
    echo -n "."
fi

# simulate a bad git command
OLD=$PATH
export PATH=test/bin/

## should fail
if ./isUpdated.sh > /dev/null 2>&1; then
    echo git should fail
    exit 1
else
    echo -n "."
fi

export PATH=$OLD
if ! ./isUpdated.sh > /dev/null 2>&1; then
    echo git command should work
    exit 1
else
    echo -n "."
fi

echo
echo OK