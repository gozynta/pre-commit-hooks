from gozynta_pc_hooks.check_python_versions_match import handle_dockerfile_line


def test_handle_dockerfile_line():
    assert handle_dockerfile_line("FROM python:3.9 ") == "3.9"
    assert handle_dockerfile_line("FROM python:3.9 as base") == "3.9"
    assert handle_dockerfile_line("FROM python:3.9-alpine") == "3.9"
    assert handle_dockerfile_line("from python:3.9-alpine") == "3.9"
    assert handle_dockerfile_line("from python") == "latest"
    assert handle_dockerfile_line("from python:foo") == "foo"
    assert handle_dockerfile_line("from somethingelse:foo") is None
