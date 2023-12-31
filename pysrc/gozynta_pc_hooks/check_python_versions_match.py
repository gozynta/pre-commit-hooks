#!/usr/bin/env python3
import pathlib
from typing import Iterator, Union, cast

import toml
import typer
import yaml

app = typer.Typer()


class VersionCheckError(Exception):
    pass


def handle_dockerfile_line(line: str) -> Union[str, None]:
    if not line.lower().startswith("from python"):
        return None

    line = line.strip()

    if ":" not in line:
        # No tag defined, dockerfile uses :latest
        return "latest"

    tag = line.split(":")[1]

    # remove ' as base'
    if " " in tag:
        tag = tag.split(" ")[0]

    if not tag[0].isdigit():
        return tag

    return tag.split("-")[0] if "-" in tag else tag


def python_version_from_dockerfile(filename: str) -> Iterator[str]:
    with open(filename, "r") as df:
        for line in df:
            if version := handle_dockerfile_line(line):
                yield version


def check_pipfile_matches(version):
    # Import this package conditionally so we can drop the dev-dependency on projects that don't use it.
    import pipfile

    pf_data = cast(dict, pipfile.load("Pipfile"))

    pipfile_python_version = pf_data["_meta"]["requires"]["python_version"].strip()

    if pipfile_python_version != version:
        raise VersionCheckError(f"Pipfile has a different python version: '{pipfile_python_version}' vs '{version}'")


def check_poetry_matches(file: pathlib.PurePath | bytes | str, version: str):
    data = toml.load(file)

    our_version = data.get("tool", {}).get("poetry", {}).get("dependencies", {}).get("python")
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
        raise VersionCheckError(
            f"In {file} poetry defines a different python version: '{our_version_orig}' vs '{version}'"
        )


def load_gitlabyaml(gitlab_yml_path: str):
    def reference_constructor(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode) -> None:
        """Dummy loader so pyyaml doesn't choke on !reference.
        https://docs.gitlab.com/ee/ci/yaml/yaml_optimization.html#reference-tags
        """
        return None

    with open(".gitlab-ci.yml", "r") as gitlab_yml:
        loader = yaml.SafeLoader
        loader.add_constructor("!reference", reference_constructor)
        return yaml.load(gitlab_yml, Loader=loader)  # nosec: B506 we're using SafeLoader


def process_files(files: list[str]):
    gitlab_variables = load_gitlabyaml(".gitlab-ci.yml")["variables"]

    gitlab_python_version = gitlab_variables["PYTHON_VERSION"].strip()

    for f in files:
        if f == "Pipfile":
            check_pipfile_matches(gitlab_python_version)
        elif f == "pyproject.toml":
            check_poetry_matches(f, gitlab_python_version)
        elif f.startswith("Dockerfile"):
            for py_version in python_version_from_dockerfile(f):
                if py_version != gitlab_python_version:
                    raise VersionCheckError(
                        f"Gitlab-ci and {f} have different python versions: '{gitlab_python_version}' vs"
                        f" '{py_version}'"
                    )


def main():
    typer.run(process_files)


if __name__ == "__main__":
    main()
