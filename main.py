#!/usr/bin/env python3
"""Entrypoint: copy entry.png (in this repo) to the output directory.

Stdlib only. Verifies the PNG magic bytes, then writes the file and
prints its sha256 so the run is auditable.
"""

import hashlib
import os
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as f:
        data = f.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("error: entry.png is not a PNG file", file=sys.stderr)
        return 1
    digest = hashlib.sha256(data).hexdigest()
    if len(data) > 1024 * 1024:
        print("error: entry.png exceeds the 1 MiB limit", file=sys.stderr)
        return 1
    with open(dst, "wb") as f:
        f.write(data)
    # Read back what was written and confirm it matches byte for byte.
    with open(dst, "rb") as f:
        written = f.read()
    if hashlib.sha256(written).hexdigest() != digest:
        print("error: written file does not match entry.png", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
