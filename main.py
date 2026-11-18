#!/usr/bin/env python3
"""Entry point for news-image-20261117.

Copies the front page this repository holds (entry.png, drawn by
build_image.py) to the grader's output directory. Standard library
only, no network, deterministic: the same bytes every run.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576


def main():
    with open(SOURCE, "rb") as fh:
        head = fh.read(len(PNG_MAGIC))
        if head != PNG_MAGIC:
            raise SystemExit("entry.png is not a PNG file")
    if os.path.getsize(SOURCE) > MAX_BYTES:
        raise SystemExit("entry.png is over the 1 MiB limit")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    print("wrote", dest, os.path.getsize(dest), "bytes")


if __name__ == "__main__":
    sys.exit(main())
