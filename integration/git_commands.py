"""
Phase 1
├── GitPython
│   ├── git-status
│   ├── git-branches
│   ├── git-log
│   └── git-summary
│
└── subprocess
    ├── git-pull
    ├── git-push
    ├── git-merge
    └── git-rebase

Phase 2
├── GitPython
│   ├── git-checkout
│   ├── git-stash
│   ├── git-remote
│   └── git-tag
│
└── subprocess
    ├── git-clone
    ├── git-add
    ├── git-commit
    └── git-diff

Phase 3
├── GitPython
│   ├── git-cherry-pick
│   ├── git-bisect
│   ├── git-reflog
│   └── git-worktree
│
└── subprocess
    ├── git-reset
    ├── git-restore
    ├── git-clean
    └── git-prune
"""

"""Git commands"""
import subprocess


class GitCommands:

    @staticmethod
    def _run(command):
        try:
            subprocess.run(command)
        except Exception as e:
            print(f"Error: {e}")
    @staticmethod
    def help():

        print("""
Git Commands

Repository
-----------
git status
git log
git summary

Branches
--------
git branches
git checkout <branch>
git tag

Remote
------
git remote
git pull
git push
git clone <repo-url>

Commits
-------
git add [path]
git commit <message>
git diff

Stash
-----
git stash
git stash-list

Merge / Rebase
--------------
git merge <branch>
git rebase <branch>

Advanced
--------
git cherry-pick <commit>
git bisect
git reflog
git worktree

Cleanup
-------
git reset
git restore <file>
git clean
git prune
""")

    def execute(self, args):
        if not args:
            self.help()
            return

        command = args[0]

        # Handle custom aliases
        if command == "summary":
            self._run(["git", "status", "--short"] + args[1:])
        elif command == "branches":
            self._run(["git", "branch"] + args[1:])
        elif command == "stash-list":
            self._run(["git", "stash", "list"] + args[1:])
        else:
            # For all other commands, pass them directly to git perfectly
            self._run(["git"] + args)

 