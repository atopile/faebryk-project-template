# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

from faebryk.core.module import Module

logger = logging.getLogger(__name__)


# Files in /modules are for application-specific modules
# Non-application-specific modules should not be placed in /modules but in /library
# If you come from a classical EDA background, think of these as hiearchical sheets


class MyApplicationModuleSubmodule(Module):
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


class MyApplicationModule(Module):
    """
    Docstring describing your module
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    submdule: MyApplicationModuleSubmodule

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
