#!/usr/bin/env python3
import re
from urllib.parse import urlparse

import toml
import typer

app = typer.Typer()
# Test with `pytest --doctest-modules dev-scripts/`


def check_for_simple_on_gar_sources(data: dict):
    """
    Make sure we don't throw keyerrors
    >>> check_for_simple_on_gar_sources({})
    >>> check_for_simple_on_gar_sources(dict(tool={}))
    >>> check_for_simple_on_gar_sources(dict(tool=dict(poetry={})))
    >>> check_for_simple_on_gar_sources(dict(tool=dict(poetry=dict(source=None))))
    >>> data_template = dict(tool=dict(poetry=dict(source=[])))
    >>> other_source = dict(name='other', url='https://example.com/foo/bar/')
    >>> good_source1 = dict(name='good1', url='https://us-python.pkg.dev/kubernetes-242623/gozynta-pipy/simple/')
    >>> good_source2 = dict(name='good2', url='https://us-east1-python.pkg.dev/kubernetes-242623/gozynta-pipy/simple')
    >>> bad_source = dict(name='bad', url='https://us-python.pkg.dev/kubernetes-242623/gozynta-pipy/')
    >>> test_data_good = data_template.copy()
    >>> test_data_good['tool']['poetry']['source'] = [other_source, good_source1, good_source2]
    >>> check_for_simple_on_gar_sources(test_data_good)
    >>> test_data_bad = data_template.copy()
    >>> test_data_bad['tool']['poetry']['source'] = [other_source, good_source1, bad_source, good_source2]
    >>> check_for_simple_on_gar_sources(test_data_bad)
    Traceback (most recent call last):
      ...
    Exception: Google Artifact Registry source 'bad', url doesn't end with '/simple/'.
    Url: 'https://us-python.pkg.dev/kubernetes-242623/gozynta-pipy/'
    """

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


def main(files: list[str]):
    for f in files:
        if f == "pyproject.toml":
            data = toml.load(f)
            check_for_simple_on_gar_sources(data)


if __name__ == "__main__":
    typer.run(main)
