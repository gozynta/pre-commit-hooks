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
- (optional) VSCode with `editorconfig.editorconfig`, `ms-python.python`, and `ms-python.vscode-pylance` extensions installed

## Dev Installation

```bash
pipenv install -d
./dev-scripts/install
```

## Usage for a new project

1. Clone this repo.  Rename the `origin` remote to `boilerplate`, and make your new Gitlab project your origin.
2. Rename pysrc/fizzbuzz.py to suit your project and start coding/testing
3. Consider removing Pipfile.lock from the .gitignore
4. Create symlink to one of the Dockerfiles (Ex: `ln -s Dockerfile.alpine Dockerfile`)
5. Update this file
6. Push to a new Gitlab project
7. Later, when there are updates to this project you can pull changes from the `boilerplate` remote to get the updates.
   - There will surely be merge conflicts, especially if this file has changed, but I think this will be an ok process overall for keeping these base files up to date?

## Notes on project structure.

The pysrc/pytest structure is based on these recommendations:
https://docs.pytest.org/en/6.2.x/goodpractices.html#tests-outside-application-code
https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure

Your project should be setup like this:
```
pysrc/
    main.py
    other_utility_script.py
    program_name/
        __init__.py
        module1.py
        module2.py
        submodule/__init__.py
        etc....
```

## Run

```bash
pipenv run ./pysrc/fizzbuzz.py
```
