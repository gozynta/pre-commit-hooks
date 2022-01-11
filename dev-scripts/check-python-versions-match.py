#!/usr/bin/env python3
from typing import Iterator, Union

import pipfile
import typer
import yaml

app = typer.Typer()

# Test with `pytest --doctest-modules dev-scripts/`


def handle_dockerfile_line(line: str) -> Union[str, None]:
    """
    >>> handle_dockerfile_line('FROM python:3.9 ')
    '3.9'
    >>> handle_dockerfile_line('FROM python:3.9-alpine')
    '3.9'
    >>> handle_dockerfile_line('from python:3.9-alpine')
    '3.9'
    >>> handle_dockerfile_line('from python')
    'latest'
    >>> handle_dockerfile_line('from python:foo')
    'foo'
    >>> handle_dockerfile_line('from somethingelse:foo')
    """
    if not line.lower().startswith("from python"):
        return None

    line = line.strip()

    if ":" not in line:
        # No tag defined, dockerfile uses :latest
        return "latest"

    tag = line.split(":")[1]
    if not tag[0].isdigit():
        return tag

    if "-" in tag:
        return tag.split("-")[0]
    else:
        return tag


def python_version_from_dockerfile(filename: str) -> Iterator[str]:
    with open(filename, "r") as df:
        for line in df:
            version = handle_dockerfile_line(line)
            if version:
                yield version


def main(files: list[str]):
    with open(".gitlab-ci.yml", "r") as gitlab_yml:
        gitlab_variables = yaml.safe_load(gitlab_yml)["variables"]

    pipfile_python_version = pipfile.load("Pipfile").data["_meta"]["requires"]["python_version"].strip()
    gitlab_python_version = gitlab_variables["PYTHON_VERSION"].strip()

    # Ensure we've defined the same python version everywhere
    if pipfile_python_version != gitlab_python_version:
        raise Exception(
            f"Pipfile and gitlab-ci have different python versions: '{pipfile_python_version}' vs"
            f" '{gitlab_python_version}'"
        )

    for f in files:
        if f.startswith("Dockerfile"):
            for py_version in python_version_from_dockerfile(f):
                if py_version != pipfile_python_version:
                    raise Exception(
                        f"Pipfile and {f} have different python versions: '{pipfile_python_version}' vs '{py_version}'"
                    )


if __name__ == "__main__":
    typer.run(main)
