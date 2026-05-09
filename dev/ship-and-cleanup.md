# Ship PR and clean up worktree


Squash-merge this PR. Then cd to the master worktree before any cleanup. From there: remove this feature worktree, delete the branch (local + remote), prune, and pull master. Chain it all so nothing runs from the dying worktree.
