# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

"""
This is the entrypoint and boilerplate of the application.
It sets up several paths and calls the app to create the graph.
Afterwards it uses the graph to export to different artifacts (e.g netlist).
"""

import logging
from pathlib import Path

import faebryk.libs.picker.lcsc as lcsc
import typer
from faebryk.core.util import get_all_modules
from faebryk.exporters.bom.jlcpcb import (
    convert_kicad_pick_and_place_to_jlcpcb,
    write_bom_jlcpcb,
)
from faebryk.exporters.esphome.esphome import make_esphome_config
from faebryk.exporters.pcb.kicad.artifacts import (
    export_dxf,
    export_gerber,
    export_glb,
    export_pick_and_place,
    export_step,
)
from faebryk.libs.app.checks import run_checks
from faebryk.libs.app.parameters import replace_tbd_with_any
from faebryk.libs.app.pcb import apply_design
from faebryk.libs.logging import setup_basic_logging
from faebryk.libs.picker.jlcpcb.pickers import add_jlcpcb_pickers
from faebryk.libs.picker.picker import pick_part_recursively
from TEMPLATE_VAR_project_name.app import MyApp
from TEMPLATE_VAR_project_name.pcb import transform_pcb
from TEMPLATE_VAR_project_name.pickers import add_app_pickers

# logging settings
logger = logging.getLogger(__name__)


def main(
    export_pcba_artifacts: bool = False,
    export_esphome_config: bool = False,  # remove if not using esphome
):
    # paths --------------------------------------------------
    build_dir = Path("./build")
    faebryk_build_dir = build_dir.joinpath("faebryk")
    faebryk_build_dir.mkdir(parents=True, exist_ok=True)
    root = Path(__file__).parent.parent.parent
    netlist_path = faebryk_build_dir.joinpath("faebryk.net")
    kicad_prj_path = root.joinpath("source")
    pcbfile = kicad_prj_path.joinpath("main.kicad_pcb")
    esphome_path = build_dir.joinpath("esphome")
    esphome_config_path = esphome_path.joinpath("esphome.yaml")
    manufacturing_artifacts_path = build_dir.joinpath("manufacturing")
    cad_path = build_dir.joinpath("cad")

    lcsc.BUILD_FOLDER = build_dir
    lcsc.LIB_FOLDER = root.joinpath("libs")

    app = MyApp()

    # fill unspecified parameters ----------------------------
    logger.info("Filling unspecified parameters")
    replace_tbd_with_any(app, recursive=True, loglvl=logging.DEBUG)

    # pick parts ---------------------------------------------
    logger.info("Picking parts")
    modules = {n.get_most_special() for n in get_all_modules(app)}
    for n in modules:
        add_jlcpcb_pickers(n, base_prio=10)
        add_app_pickers(n)
    pick_part_recursively(app)

    # graph --------------------------------------------------
    logger.info("Make graph")
    G = app.get_graph()

    # checks -------------------------------------------------
    logger.info("Running checks")
    run_checks(app, G)

    # pcb ----------------------------------------------------
    logger.info("Make netlist & pcb")
    apply_design(pcbfile, netlist_path, G, app, transform_pcb)

    # generate pcba manufacturing and other artifacts ---------
    if export_pcba_artifacts:
        logger.info("Exporting PCBA artifacts")
        write_bom_jlcpcb(
            get_all_modules(app),
            manufacturing_artifacts_path.joinpath("jlcpcb_bom.csv"),
        )
        export_step(pcbfile, step_file=cad_path.joinpath("pcba.step"))
        export_glb(pcbfile, glb_file=cad_path.joinpath("pcba.glb"))
        export_dxf(pcbfile, dxf_file=cad_path.joinpath("pcba.dxf"))
        export_gerber(
            pcbfile, gerber_zip_file=manufacturing_artifacts_path.joinpath("gerber.zip")
        )
        pnp_file = manufacturing_artifacts_path.joinpath("pick_and_place.csv")
        export_pick_and_place(pcbfile, pick_and_place_file=pnp_file)
        convert_kicad_pick_and_place_to_jlcpcb(
            pnp_file,
            manufacturing_artifacts_path.joinpath("jlcpcb_pick_and_place.csv"),
        )

    # esphome config -----------------------------------------
    # Remove if not using esphome
    if export_esphome_config:
        logger.info("Generating esphome config")
        esphome_config = make_esphome_config(G)
        esphome_config_path.write_text(esphome_config, encoding="utf-8")


if __name__ == "__main__":
    setup_basic_logging()
    typer.run(main)
