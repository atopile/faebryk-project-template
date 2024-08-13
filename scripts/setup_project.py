#!/usr/bin/env python3

import datetime
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import typer

PREFIX = "TEMPLATE_VAR_"


@dataclass
class Var:
    key: str
    description: str

    lower_case: bool = False
    valid_python_name: bool = False
    no_prompt: bool = False
    regex: str | None = None

    transform: Callable[[str], str] | None = None


VARS = [
    Var(
        "project_name",
        "pip/package name of the project",
        lower_case=True,
        valid_python_name=True,
    ),
    Var("short_description", "Small one-line description of the project"),
    Var(
        "author",
        "Appears in pip and license. Format 'Your Name <Your Email>'"
        "(e.g 'John Doe <john@doe.net>')",
    ),
    Var(
        "github",
        "<owner|org>/<repo>",
        regex=r"^[a-zA-Z0-9-]+/[a-zA-Z0-9-]+$",
    ),
    Var("gh_user", "Your github username"),
    Var(
        "year",
        "",
        no_prompt=True,
        transform=lambda _: str(datetime.datetime.now().year),
    ),
]

FILES = [
    "src",
    "docs",
    "LICENSE",
    "pyproject.toml",
    "README_template.md",
]

CACHE_FILE_PATH = Path("/tmp/app_template_cache.json")


def move_file_and_delete_empty_parent(old: Path, new: Path):
    new.parent.mkdir(parents=True, exist_ok=True)
    old.rename(new)

    for p in old.parents:
        if not list(p.glob("*")):
            p.rmdir()


def main(cache: bool = True, dry_run: bool = False):
    replacements = {}

    if cache and CACHE_FILE_PATH.exists():
        replacements = json.loads(CACHE_FILE_PATH.read_text())
        print("Warning: using cached values:", replacements)

    for var in VARS:
        key = f"{PREFIX}{var.key}"
        value = ""
        if key in replacements:
            continue

        while True:
            if not var.no_prompt:
                value = typer.prompt(var.description)

            if var.transform:
                value = var.transform(value)

            if var.lower_case:
                value_post = value.lower()
                if value_post != value:
                    print(
                        "Warning: converting to lower case: " f"{value} -> {value_post}"
                    )
                value = value_post

            if var.valid_python_name:
                value_post = value.replace("-", "_")
                if value_post != value:
                    print(
                        "Warning: converting to python name: "
                        f"{value} -> {value_post}"
                    )
                value = value_post

            if var.regex:
                if not re.match(var.regex, value):
                    print(f"Invalid value: {value}")
                    continue

            replacements[key] = value
            CACHE_FILE_PATH.write_text(json.dumps(replacements))
            break

    # Get files --------------------------------------------------
    root = Path(__file__).parent.parent
    files: list[Path] = []
    for path_name in FILES:
        path = root.joinpath(path_name)
        if path.is_dir():
            files.extend(p for p in path.rglob("*") if p.is_file())
        else:
            files.append(path)

    # Replace vars --------------------------------------------------
    for f in files:
        text = f.read_text()
        out_path = f.relative_to(root)

        # Replace in text
        for k, v in replacements.items():
            if k in text:
                print(f"Replacing  in {f}: |{k}| -> |{v}|")
                text = text.replace(k, v)
            if k in str(out_path):
                out_path = Path(str(out_path).replace(k, v))

        out_path = root / out_path

        # Replace in path
        if out_path != f:
            print(f"Renaming {f.relative_to(root)} -> {out_path.relative_to(root)}")
            if not dry_run:
                move_file_and_delete_empty_parent(f, out_path)

        if not dry_run:
            out_path.write_text(text)

    # Remove template files ----------------------------------------
    (root / "README.md").unlink()
    (root / "README_template.md").rename(root / "README.md")


if __name__ == "__main__":
    typer.run(main)
