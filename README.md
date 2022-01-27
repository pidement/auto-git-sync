# auto-git-sync

[![Build Status](https://app.travis-ci.com/FriendDementor/auto-git-sync.svg?branch=main)](https://app.travis-ci.com/FriendDementor/auto-git-sync)

You should have installed git on the system, the environment variable ```AUTO_GIT_SYNC_BRANCH``` with a valid remote branch name and run these scripts on an repository that can read the data from the default remote name.

```
#!/bin/sh
# isUpdated.sh
```

```
#!/bin/sh
# update.sh
```

```
if isUpdated.sh; then killServer.sh && update.sh fi;; startServerIfClosed.sh
```

```
killServer.sh && update.sh && startServer.sh
```

#test

