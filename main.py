#!/usr/bin/env python3
"""Entrypoint for the news-image-20261125 entry.

Running this file builds the front page: it executes the composition
module (make_front_page.py), which renders "The Daily Globe" for
Wednesday, November 25, 2026 and writes entry.png beside this file.

Usage: python3 main.py [output.png]
An optional argument copies the finished page to that path as well.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENTRY = os.path.join(HERE, "entry.png")


def main(argv):
    # The composition runs at import time and saves entry.png itself.
    sys.path.insert(0, HERE)
    import make_front_page  # noqa: F401  (importing it builds the page)

    if len(argv) > 1:
        target = os.path.abspath(argv[1])
        if target != ENTRY:
            shutil.copyfile(ENTRY, target)
            print("copied", ENTRY, "->", target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
