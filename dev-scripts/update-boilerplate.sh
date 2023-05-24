#!/bin/bash

# This script updates the boilerplate submodule to the latest version
#
# Usage:
#   ./update-boilerplate.sh <boilerplate-branch>
#
#  - boilerplate-branch: (optional) The branch of the boilerplate repo to use. Defaults to main.

# Exit on error
set -e
# Print commands
set -x
# Fail on pipefail
set -o pipefail

# Make sure there's no uncommitted git changes
if [[ -n $(git status --porcelain) ]]; then
    set +x
    echo -e "\e[31mThere are uncommitted changes in the repository. Please \e[1mcommit or stash them\e[22m before running this script.\e[0m"
    exit 1
fi

# get starting commit
STARTING_COMMIT=$(git rev-parse HEAD)

(git remote | grep boilerplate) || git remote add boilerplate "git@gitlab.com:gozynta/project-templates/boilerplate.git"

git fetch --all
# If $1 contains a branch name, then pull from that branch. Otherwise, pull from main.
git pull --rebase=false --no-ff boilerplate ${1:-main} || true

if [[ -n $(git status --porcelain poetry.lock) ]]; then
    git checkout $STARTING_COMMIT -- poetry.lock
    if [[ -n $(git status --porcelain pyproject.toml) ]]; then
        set +x
        echo -e "\e[31mCan't auto-resolve poetry.lock changes\e[0m, merge pyproject.toml then run '\e[96mpoetry lock --no-update\e[0m'"
    else
        poetry lock --no-update
        git add poetry.lock
    fi
fi

set +x
echo -e "\e[32mBoilerplate changes stages for commit. \e[36mPlease review, resolve conflicts, and then commit.\e[0m"
