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

## Run

```bash
pipenv run ./pysrc/fizzbuzz.py
```
