# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F
from faebryk.core.module import Module

from TEMPLATE_VAR_project_name.library.my_library_module import MyLibraryModule
from TEMPLATE_VAR_project_name.modules.my_application_module import MyApplicationModule

logger = logging.getLogger(__name__)

"""
This file is for the top-level application modules.
This should be the entrypoint for collaborators to start in to understand your project.
Treat it as the high-level design of your project.
Avoid putting any generic or reusable application modules here.
Avoid putting any low-level modules or parameter specializations here.
"""


class MyApp(Module):
    """
    Docstring describing your app
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    submodule: MyApplicationModule
    my_part: MyLibraryModule
    # ----------------------------------------
    #                 traits
    # ----------------------------------------

    def __preinit__(self):
        # ------------------------------------
        #           connections
        # ------------------------------------

        # ------------------------------------
        #            net names
        # ------------------------------------
        nets = {
            # "in_5v": ...power.hv,
            # "gnd": ...power.lv,
        }
        for net_name, mif in nets.items():
            net = F.Net.with_name(net_name)
            net.IFs.part_of.connect(mif)

        # ------------------------------------
        #           specialize
        # ------------------------------------

        # ------------------------------------
        #          parametrization
        # ------------------------------------
