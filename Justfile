pytest:
    #!/bin/bash
    poetry run pytest

self_run:
    # Runs the pre-commit hooks on the current repository
    #!/bin/bash
    set -e # exit on error
    pre-commit try-repo . check-poetry-sources --all-files
    pre-commit try-repo . check-python-versions-match --all-files

test: pytest self_run
