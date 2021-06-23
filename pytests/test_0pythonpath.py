import pathlib
import sys


def test_pythonpath():
    """Ensure that the pysrc directory is in the PYTHONPATH

    If it's not then later tests will fail, but this will print some better debugging info.
    """
    print(sys.path)
    pysrc_path = pathlib.Path(__file__).parent.parent.joinpath("pysrc").absolute()
    assert str(pysrc_path) in sys.path
