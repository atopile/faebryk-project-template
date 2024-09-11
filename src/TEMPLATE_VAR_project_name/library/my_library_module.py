# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.units import P  # noqa: F401

logger = logging.getLogger(__name__)


# Files in /library are for non-application-specific modules
# These files are mostly good candidates for upstreaming to faebryk
# Application specific modules should not be placed in /library but in /modules
# Only one module per file
# For typical library module examples check out faebryk.library


# TIP: To (quickly) add more library modules use
# `python -m faebryk.tools.libadd module <name>`


class MyLibraryModule(Module):
    """
    Docstring describing your module
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------

    # ----------------------------------------
    #                 traits
    # ----------------------------------------

    def __preinit__(self):
        # ------------------------------------
        #           connections
        # ------------------------------------

        # ------------------------------------
        #          parametrization
        # ------------------------------------
        pass
