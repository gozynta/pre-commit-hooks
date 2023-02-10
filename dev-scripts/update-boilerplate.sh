#!/bin/bash

# This script updates the boilerplate submodule to the latest version

# Exit on error
set -e
# Print commands
set -x
# Fail on pipefail
set -o pipefail

# Make sure there's no uncommitted git changes
if [[ -n $(git status --porcelain) ]]; then
    echo "There are uncommitted changes in the repository. Please commit or stash them before running this script."
    exit 1
fi

# get starting commit
STARTING_COMMIT=$(git rev-parse HEAD)

(git remote | grep boilerplate) || git remote add boilerplate "git@gitlab.com:gozynta/project-templates/boilerplate.git"

git fetch --all
git pull --rebase=false --no-ff boilerplate main || true

if [[ -n $(git status --porcelain poetry.lock) ]]; then
    git checkout $STARTING_COMMIT -- poetry.lock
    if [[ -n $(git status --porcelain pyproject.toml) ]]; then
        echo "Can't auto-resolve poetry.lock changes, fix pyproject.toml then run 'poetry lock --no-update'"
    else
        poetry lock --no-update
        git add poetry.lock
    fi
fi

echo "Boilerplate changes stages for commit. Please review, resolve conflicts, and then commit."
