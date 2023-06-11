#!/usr/bin/env python3
import re
from urllib.parse import urlparse

import toml
import typer

app = typer.Typer()


def check_for_simple_on_gar_sources(data: dict):
    sources = data.get("tool", {}).get("poetry", {}).get("source", [])
    if not sources:
        return

    for source in sources:
        url = urlparse(source.get("url", ""))
        if url.hostname and url.hostname.endswith("python.pkg.dev") and not re.search("/simple/?$", url.path):
            raise Exception(
                f"Google Artifact Registry source '{source['name']}', url doesn't end with '/simple/'.\n"
                f"Url: '{source['url']}'"
            )


def process_files(files: list[str]):
    for f in files:
        if f == "pyproject.toml":
            data = toml.load(f)
            check_for_simple_on_gar_sources(data)


def main():
    typer.run(process_files)


if __name__ == "__main__":
    main()
