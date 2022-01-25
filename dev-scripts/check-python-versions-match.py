#!/usr/bin/env python3
import os
from typing import Iterator, Union

# To toml or to tomli?
# Black uses tomli so we should always have it.
# Everything else seems to use toml so we should always have that too.
# tomli is smaller, so use that, but if it stops being in our environment then switch to toml.
import toml
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


def test_pipfile_matches(version):
    # Import this package conditionally so we can drop the dev-dependency on projects that don't use it.
    import pipfile

    pipfile_python_version = pipfile.load("Pipfile").data["_meta"]["requires"]["python_version"].strip()

    if pipfile_python_version != version:
        raise Exception(f"Pipfile has a different python version: '{pipfile_python_version}' vs '{version}'")


def test_poetry_matches(file: os.PathLike, version: str):
    data = toml.load(file)

    our_version = data.get("tool", dict()).get("poetry", dict()).get("dependencies", dict()).get("python")
    if not our_version or our_version == "*":
        # No poetry/python version specified, so nothing to check
        return

    our_version_orig = our_version

    # Trim all the version restriction indicators.
    # Ideally this would be smarter and make sure that if poetry specifies a version range that the gitlab-ci version
    # remains within that range.
    our_version = our_version.lstrip("^~<>!= ")

    # Turn 3.6.7 into 3.6
    our_version = ".".join(our_version.split(".")[:2])

    if our_version != version:
        raise Exception(f"In {file} poetry defines a different python version: '{our_version_orig}' vs '{version}'")


def main(files: list[str]):
    with open(".gitlab-ci.yml", "r") as gitlab_yml:
        gitlab_variables = yaml.safe_load(gitlab_yml)["variables"]

    gitlab_python_version = gitlab_variables["PYTHON_VERSION"].strip()

    for f in files:
        if f == "Pipfile":
            test_pipfile_matches(gitlab_python_version)
        elif f == "pyproject.toml":
            test_poetry_matches(f, gitlab_python_version)
        elif f.startswith("Dockerfile"):
            for py_version in python_version_from_dockerfile(f):
                if py_version != gitlab_python_version:
                    raise Exception(
                        f"Gitlab-ci and {f} have different python versions: '{gitlab_python_version}' vs"
                        f" '{py_version}'"
                    )


if __name__ == "__main__":
    typer.run(main)
