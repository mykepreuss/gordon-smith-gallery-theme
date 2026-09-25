#!/bin/sh
# Push the current branch over SSH and open GitHub's pull request form.
# An agent that prepared the branch leaves the title and description in
# .git/pr/<branch>.title and .git/pr/<branch>.md (inside .git, so never committed).
# DRY_RUN=1 prints the pull request link without pushing.
set -e
cd "$(git rev-parse --show-toplevel)"
branch=$(git rev-parse --abbrev-ref HEAD)
if [ "$branch" = "main" ]; then
  echo "You're on main. Changes go through a branch and a pull request (AGENTS.md)." >&2
  exit 1
fi
enc() { perl -0777 -pe 's/([^A-Za-z0-9._~-])/sprintf("%%%02X", ord($1))/ge'; }
pr=".git/pr/$(printf %s "$branch" | tr / _)"
url="https://github.com/mykepreuss/gordon-smith-gallery-theme/compare/main...$branch?quick_pull=1"
if [ -f "$pr.title" ]; then url="$url&title=$(printf %s "$(cat "$pr.title")" | enc)"; fi
if [ -f "$pr.md" ]; then url="$url&body=$(enc < "$pr.md")"; fi
if [ "${DRY_RUN:-}" = 1 ]; then echo "$url"; exit 0; fi
git push -u origin "$branch"
open "$url"
