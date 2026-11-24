#!/usr/bin/env python3
"""news-23 b66 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only. Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import hashlib
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAX_BYTES = 1024 * 1024


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    sys.exit(1)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    here_abs = os.path.abspath(HERE)
    if out_dir_abs == here_abs or out_dir_abs.startswith(here_abs + os.sep):
        fail("MAKEFUN_OUTPUT_DIR must not be inside the repo (%s)" % out_dir_abs)
    if not os.path.isfile(SRC):
        fail("source entry.png missing: %s" % SRC)

    with open(SRC, "rb") as f:
        data = f.read()

    # PNG checks: signature, IHDR 1024x1024, IEND trailer, size cap.
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("not a PNG file")
    if len(data) < 33 or data[12:16] != b"IHDR":
        fail("missing IHDR chunk")
    width, height, depth, ctype = struct.unpack(">IIBB", data[16:26])
    if (width, height) != (1024, 1024):
        fail("entry.png must be 1024x1024, got %dx%d" % (width, height))
    if depth != 8 or ctype not in (2, 6):
        fail("unexpected bit depth %d / colour type %d" % (depth, ctype))
    if data[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        fail("missing well-formed IEND trailer")
    if len(data) > MAX_BYTES:
        fail("entry.png is %d bytes, over the 1 MiB cap" % len(data))

    os.makedirs(out_dir_abs, exist_ok=True)
    dst = os.path.join(out_dir_abs, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)

    # Re-read the output and confirm it is byte-identical to the source.
    with open(dst, "rb") as f:
        written = f.read()
    if written != data:
        fail("output differs from source after copy")
    sha = hashlib.sha256(data).hexdigest()
    print("source entry.png: %dx%d, %d bytes, sha256 %s" % (width, height, len(data), sha))
    print("wrote %s (%d bytes, sha256 %s)" % (dst, len(data), sha))


if __name__ == "__main__":
    main()
