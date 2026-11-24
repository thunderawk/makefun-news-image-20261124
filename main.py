#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261124.

Copies the pre-rendered front page (entry.png, in this repo) to
/output/entry.png. Stdlib only, no network, deterministic.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main():
    src = os.path.join(HERE, "entry.png")
    os.makedirs(OUT, exist_ok=True)
    shutil.copyfile(src, os.path.join(OUT, "entry.png"))


if __name__ == "__main__":
    main()
