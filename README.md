# Boilerplate for New Projects

## Overview
A boilerplate Python 3 project set up for unit tests and continuous integration.

Specifically:

- Enforces Python style rules with black and flake8
- Sorts imports with isort
- Configures VSCode to use black, flake8, and isort from the pipenv
- git pre-commit hook to check code standards before commits are created
- Sample Dockerfile
- Standard set of dev dependencies for poetry including library building

## Dev Prerequisites
- python 3.9
- poetry  `sudo apt install pipx && pipx install poetry`
- (optional) VSCode with `editorconfig.editorconfig`, `ms-python.python`, and `ms-python.vscode-pylance` extensions installed

## Dev Installation

```bash
poetry install
./dev-scripts/install
```

## Converting your project from pipenv to poetry

```bash
# Review the pyproject.toml, make sure it contains all the boilerplate from this project
#   Update name, version, and packages

# Install Poetry and pipenv-poetry-migrate if you don't have them
sudo apt install pipx
pipx install "poetry>=1.2.0a2"
pipx install pipenv-poetry-migrate

# Convert dependencies
pipenv-poetry-migrate -f Pipfile -t pyproject.toml

# Cleanup
rm .venv
pipenv --rm
poetry remove -D pipfile
rm Pipfile Pipfile.lock

# Generate poetry.lock
poetry lock

# Update your Dockerfiles to install w/ Poetry instead of Pipenv (see the ones in boilerplate)
```

## Usage for a new project
1. Create gitlab project
  - Option a: Create using gitlab template
    - Create new project in Gitlab
    - Select "Create from template"
    - Choose this template from the "group" tab
    - Clone your new project from gitlab.
  - Option b: Manually create new project
     - Clone this repo.
     - Rename the origin remote to boilerplate:
        `git remote rename origin boilerplate`
     - Make your new Gitlab project
     - Set your origin:
        `git remote add origin <url>`
     - Push to your new Gitlab project:
        `git push -u origin main`
2. Rename pysrc/fizzbuzz.py to suit your project and start coding/testing
3. Consider adding poetry.lock to the .gitignore (IE: if you're building a shared library)
4. Create symlink to one of the Dockerfiles (Ex: `ln -s Dockerfile.alpine Dockerfile`)
5. Update this file
6. Later, when there are updates to this project you can pull changes from the `boilerplate` remote to get the updates.

## Updating an existing project
1. Make sure this repo is set up as a remote:
    `bash -c '(git remote |grep boilerplate) || git remote add boilerplate "git@gitlab.com:gozynta/project-templates/boilerplate.git"'`
2. Update the remote
    `git fetch --all`
3. Pull changes from this repo. (Note: This is the exception to our usual rule of "no merge commits".  That ensures that projects using this repo will keep track of what changes from here have/haven't been merged.  Rebasing your project on this repo would be a big mess, and cherry-picking commits from here is very error-prone: manual, unclear what was picked before, and still requires fixing merge conflicts).
    `git pull --rebase=false --no-ff boilerplate main`
4. Now you will likely have a bunch of merge conflicts to go through.  Please carefully consider each of these.  The one exception is the .lock files.  I'd recommend going back to your previous version of the lock, and then updating it.  `git checkout <yourbranch> -- poetry.lock && poetry lock`
5. Push your branch, etc as usual.  Just DO NOT do a rebase on your branch AND make sure Gitlab DOES NOT squash your commits.

## Notes on project structure.

The pysrc/pytest structure is based on these recommendations:
https://docs.pytest.org/en/6.2.x/goodpractices.html#tests-outside-application-code
https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure

Your project should be setup like this:
(the ony .py files that should be directly in pysrc/ are scripts that are run but never imported)
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
poetry run ./pysrc/fizzbuzz
```
