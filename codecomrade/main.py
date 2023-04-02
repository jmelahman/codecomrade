#!/usr/bin/env python3
from __future__ import annotations

import functools
import pathlib
import shutil
import subprocess
from typing import List

import click
import codeowners


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument("owners", nargs=-1)
@click.option("--toplevel")
def diff(owners: List[str], toplevel: str) -> None:
    run_diff(owners, toplevel)


@cli.command()
@click.argument("files", nargs=-1)
@click.option("--toplevel")
def list(files: List[str], toplevel: str) -> None:
    list_all(files, toplevel)


class Comrade:
    def __init__(self, toplevel: str | None = None) -> None:
        git = shutil.which("git")
        if git is None:
            raise RuntimeError("git is not installed")
        self._git = git
        self._toplevel = toplevel

    @functools.cached_property
    def toplevel(self) -> pathlib.Path:
        if self._toplevel is not None:
            return pathlib.Path(self._toplevel)
        return pathlib.Path(
            subprocess.check_output([self._git, "rev-parse", "--show-toplevel"])
            .decode()
            .strip()
        )

    @functools.cached_property
    def owners(self) -> codeowners.CodeOwners:
        return codeowners.CodeOwners(
            pathlib.Path(self.toplevel / ".github" / "CODEOWNERS").read_text()
        )

def run_diff(owners: List[str], toplevel: str) -> None:
    comrade = Comrade(toplevel)
    changed_files = (
        subprocess.check_output([comrade._git, "-C", comrade.toplevel, "diff", "--name-only"])
        .decode()
        .rstrip("\n")
        .split("\n")
    )
    for changed_file in changed_files:
        owners_tuple = comrade.owners.of(changed_file)
        if owners and owners_tuple and any(owner in owners for _, owner in owners_tuple):
            print(changed_file)
        elif not owners and not owners_tuple:
            print(changed_file)


def list_all(files: List[str], toplevel: str) -> None:
    seen_owners = set()
    comrade = Comrade(toplevel)
    for fname in files:
        for owner_tuple in comrade.owners.of(fname):
            owner = owner_tuple[1]
            if owner not in seen_owners:
                print(owner)
            seen_owners.add(owner)
    if files:
        return
    
    for path in comrade.owners.paths:
        for owner_tuple in path[2]:
            _, owner = owner_tuple
            if owner not in seen_owners:
                seen_owners.add(owner)
                print(owner)
