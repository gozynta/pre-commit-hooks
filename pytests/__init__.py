import pathlib
import sys

# insert the pysrc directory into the path, modules will be loaded from there, e.g. pysrc/mymodule1, pysrc/mymodule2
pysrc_path = pathlib.Path(__file__).parent.parent.joinpath("pysrc").absolute()
sys.path.insert(0, str(pysrc_path))
