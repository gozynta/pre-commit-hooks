# Pre-commit Hooks

## Overview
Some pre-commit hooks to help keep our code clean and consistent.

### check_poetry_sources
Checks that all Google Artifact Registry sources are using the simple url format.

This is a very easy mistake to make, and the error is very unclear when they aren't meaning it can take a long time to
troubleshoot.

### check_python_versions_match
Check that we're specifying the same python version in:
- Dockerfiles that use FROM python
- Pipfile
- Poetry (pyproject.toml [tool.poetry.dependencies])
- .gitlab-ci.yml PYTHON_VERSION variable

# Usage
Add the following to your .pre-commit-config.yaml
```yaml
  - repo: https://github.com/gozynta/pre-commit-hooks
    rev: ""
    hooks:
      - id: check-poetry-sources
      - id: check-python-versions-match
```

## Dev Prerequisites
- python 3.10
- poetry
- just

## Dev Installation
```bash
# Initialize poetry
poetry install --with=dev

# Install git pre-commit hooks
./dev-scripts/install
```

## Testing

```bash
just test
```
