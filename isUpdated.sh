#!/bin/bash

# Check if environment variable was defined
if [[ -z "${AUTO_GIT_SYNC_BRANCH}" ]]; then
    >&2 echo "Environment variable AUTO_GIT_SYNC_BRANCH do not defined."
    exit 1
else
    AUTO_GIT_SYNC_BRANCH="${AUTO_GIT_SYNC_BRANCH}"
fi

# Check if git it's installed
if ! git --version > /dev/null 2>&1; then
    >&2 echo "git command not found"
    exit 1
fi

# Check if the working dir it's a git repo
if ! git status > /dev/null 2>&1; then
    >&2 echo "git repo not found"
    exit 1
fi

echo "AUTO_GIT_SYNC_BRANCH value is $AUTO_GIT_SYNC_BRANCH"