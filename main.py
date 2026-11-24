#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261124.

Copies the pre-rendered front page (entry.png, in this repo) to
/output/entry.png. Stdlib only, no network, deterministic.
"""
import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    src = os.path.join(HERE, "entry.png")
    with open(src, "rb") as f:
        data = f.read()
    if not data.startswith(PNG_MAGIC):
        raise SystemExit("entry.png is not a PNG")
    os.makedirs(OUT, exist_ok=True)
    dst = os.path.join(OUT, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    print("entry.png %d bytes sha256 %s"
          % (len(data), hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
