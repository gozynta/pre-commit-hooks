import os
import sys

import pipfile
import sh
import yaml
from dotenv import load_dotenv

load_dotenv()


def run_command(*args):
    """
    Run build commands from the shell even though we could hook into their python APIs since this will lead to more
    consistency with what's being run in the CI"""

    # Want to print the commmand before running it, like `set -x`.  This is very niave, but at least gets the idea
    # across.  A more accurate command line will be printed if a command fails.
    print(f'+ {" ".join(args)}')
    try:
        sh.Command(args[0])(args[1:], _fg=True)
    except sh.ErrorReturnCode as err:
        print(f"`{err.full_cmd}` failed")
        sys.exit(err.exit_code)  # type: ignore


# Start with checking our build scripts
run_command("isort", "-c", "dev-scripts")
run_command("black", "--check", "--diff", "--color", "dev-scripts")

# Delete pyc files from previous builds.
run_command(
    "find",
    ".",
    "-name",
    "*.pyc",
    "-type",
    "f",
    "-delete",
)

# load variables we'll need later
with open(".gitlab-ci.yml", "r") as gitlab_yml:
    gitlab_variables = yaml.safe_load(gitlab_yml)["variables"]

python_version = pipfile.load("Pipfile").data["_meta"]["requires"]["python_version"]
source_dir = gitlab_variables.get("PYTHON_SOURCE_PATH", "./pysrc/")
test_dir = gitlab_variables.get("PYTHON_TEST_PATH", "pytests/")
os.environ["PYTHONPATH"] = source_dir

# Ensure we've defined the same python version everywhere
assert python_version == gitlab_variables["PYTHON_VERSION"]

run_command("bash", "-c", "echo $PYTHON_PATH")

# TODO: This isn't very DRY, since we're having to define the same default variables and commands both here and in
# https://gitlab.com/gozynta/gcloud-tagging-docker/-/blob/master/gitlab-ci-template.yml
run_command("isort", "-c", source_dir)
run_command("black", "--check", "--diff", "--color", source_dir)
run_command("flake8", source_dir, test_dir)

# Run tests under coverage
run_command("coverage", "run", f"--source={source_dir}", "-m", "pytest", test_dir)
run_command("coverage", "report", "-m")
