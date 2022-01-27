#!/usr/bin/bash

if [[ -z "${AUTO_GIT_SYNC_BRANCH}" ]]; then
  echo "Environment variable AUTO_GIT_SYNC_BRANCH do not defined."
  exit 1
else
  AUTO_GIT_SYNC_BRANCH="${AUTO_GIT_SYNC_BRANCH}"
fi

echo "AUTO_GIT_SYNC_BRANCH value is $AUTO_GIT_SYNC_BRANCH"