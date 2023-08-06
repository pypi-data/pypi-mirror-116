""" BioSimulators-compliant command-line interface to the `pyNeuroML <https://github.com/NeuroML/pyNeuroML>`_ simulation program.

:Author: Jonathan Karr <karr@mssm.edu>
:Date: 2021-05-28
:Copyright: 2021, BioSimulators Team
:License: MIT
"""

from .._version import __version__
from ..core import exec_sedml_docs_in_combine_archive
from ..data_model import Simulator
from biosimulators_utils.simulator.cli import build_cli
import functools
import pyneuroml


def main(argv=None):
    """ Run the command-line interface to pyNeuroML

    Args:
        argv (:obj:`list` of :obj:`str`, optional): command-line arguments
    """
    App = build_cli('pyneuroml', __version__,
                    'pyNeuroML', pyneuroml.__version__, 'https://github.com/NeuroML/pyNeuroML',
                    functools.partial(exec_sedml_docs_in_combine_archive, simulator=Simulator.pyneuroml))

    with App(argv=argv) as app:
        app.run()


if __name__ == "__main__":
    main()
