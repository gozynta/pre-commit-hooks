import pytest

from gozynta_pc_hooks.check_poetry_sources import check_for_simple_on_gar_sources


def test_check_for_simple_on_gar_sources():
    # Make sure we don't throw keyerrors
    check_for_simple_on_gar_sources({})
    check_for_simple_on_gar_sources(dict(tool={}))
    check_for_simple_on_gar_sources(dict(tool=dict(poetry={})))
    check_for_simple_on_gar_sources(dict(tool=dict(poetry=dict(source=None))))
    data_template = dict(tool=dict(poetry=dict(source=[])))
    other_source = dict(name="other", url="https://example.com/foo/bar/")
    good_source1 = dict(name="good1", url="https://us-python.pkg.dev/kubernetes-242623/gozynta-pipy/simple/")
    good_source2 = dict(name="good2", url="https://us-east1-python.pkg.dev/kubernetes-242623/gozynta-pipy/simple")
    bad_source = dict(name="bad", url="https://us-python.pkg.dev/kubernetes-242623/gozynta-pipy/")
    test_data_good = data_template.copy()
    test_data_good["tool"]["poetry"]["source"] = [other_source, good_source1, good_source2]
    check_for_simple_on_gar_sources(test_data_good)
    test_data_bad = data_template.copy()
    test_data_bad["tool"]["poetry"]["source"] = [other_source, good_source1, bad_source, good_source2]

    with pytest.raises(
        Exception,
        match=(
            "Google Artifact Registry source 'bad', url doesn't end with '/simple/'.\nUrl:"
            " 'https://us-python.pkg.dev/kubernetes-242623/gozynta-pipy/'"
        ),
    ):
        check_for_simple_on_gar_sources(test_data_bad)
