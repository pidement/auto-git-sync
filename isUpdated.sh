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

# Get remote name
if [[ $(git remote | wc -l) -eq 1 ]]; then
    REMOTE_NAME=$(git remote)
else
    >&2 echo "remote do not defined"
    exit 1
fi

# Fetch all remote refs
git fetch $REMOTE_NAME > /dev/null 2>&1;

# Get remote hash
if git rev-parse origin/$AUTO_GIT_SYNC_BRANCH > /dev/null 2>&1; then
    REMOTE_HASH=$(git rev-parse origin/"$AUTO_GIT_SYNC_BRANCH")
else
    >&2 echo "branch do not exists on remote"
    exit 1
fi

# Update all branches
git remote update > /dev/null 2>&1;

# Check if HEAD it's defined
if ! git rev-parse HEAD > /dev/null 2>&1;then
    >&2 echo "HEAD do not defined"
    exit 1
else
    LOCAL_HASH=$(git rev-parse HEAD)
fi

# Check if we should update
if [[ "$LOCAL_HASH" = "$REMOTE_HASH" ]]; then
    echo "Updated."
    exit 1
else
    echo "Should update."
    exit
fi
