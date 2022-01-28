#!/usr/bin/bash

if [[ -z "${AUTO_GIT_SYNC_BRANCH}" ]]; then
    >&2 echo "Environment variable AUTO_GIT_SYNC_BRANCH do not defined."
    exit 1
else
    AUTO_GIT_SYNC_BRANCH="${AUTO_GIT_SYNC_BRANCH}"
fi


if ! git --version > /dev/null 2>&1; then
    >&2 echo "git command not found"
    exit 1
fi

echo "AUTO_GIT_SYNC_BRANCH value is $AUTO_GIT_SYNC_BRANCH"