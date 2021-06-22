# Boilerplate for New Projects

## Overview
A boilerplate Python 3 project set up for unit tests and continuous integration.

Specifically:

- Enforces Python style rules with black and flake8
- Sorts imports with isort
- Configures VSCode to use black, flake8, and isort from the pipenv
- git pre-commit hook to check code standards before commits are created

## Dev Prerequisites
- python 3.9
- pipenv
- (optional) VSCode with `ms-python.python` and `ms-python.vscode-pylance` extensions installed

## Dev Installation

```bash
pipenv install -d
./dev-scripts/enable-git-hooks
```

## Usage for a new project

1. Clone this repo.  Rename the `origin` remote to `boilerplate`, and make your new Gitlab project your origin.
2. Rename pysrc/fizzbuzz.py to suit your project and start coding/testing
3. Consider removing Pipfile.lock from the .gitignore
4. Update this file
5. Push to a new Gitlab project
6. Later, when there are updates to this project you can pull changes from the `boilerplate` remote to get the updates.
   - There will surely be merge conflicts, especially if this file has changed, but I think this will be an ok process overall for keeping these base files up to date?

## Run

```bash
pipenv run ./pysrc/fizzbuzz.py
```
