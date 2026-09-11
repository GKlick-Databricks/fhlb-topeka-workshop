"""Tiny notebook builder for the FAA wildlife-strike workshop.

Author notebooks as a list of cells: md("...") for markdown, code("...") for code,
sql("...") for a %sql code cell (prepends the magic). write_nb(path, cells) emits
valid nbformat-4 JSON that imports cleanly into Databricks.
"""
import json, os


def md(source: str):
    return {"cell_type": "markdown", "metadata": {}, "source": _lines(source)}


def code(source: str):
    return {"cell_type": "code", "metadata": {}, "execution_count": None,
            "outputs": [], "source": _lines(source)}


def sql(source: str):
    src = source if source.lstrip().startswith("%sql") else "%sql\n" + source
    return code(src)


def _lines(s: str):
    s = s.strip("\n")
    lines = s.split("\n")
    return [l + "\n" for l in lines[:-1]] + [lines[-1]] if lines else [""]


def write_nb(path: str, cells):
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(nb, f, indent=1)
    # sanity: re-parse
    with open(path) as f:
        json.load(f)
    print("wrote", path, f"({len(cells)} cells)")
