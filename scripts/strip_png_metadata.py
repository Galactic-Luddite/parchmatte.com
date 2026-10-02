#!/usr/bin/env python3
"""Copy an 8-bit RGB/RGBA screenshot without ancillary PNG metadata.

The image header and compressed pixel chunks are preserved byte for byte.
Usage: python3 scripts/strip_png_metadata.py INPUT.png OUTPUT.png
"""

import argparse
import struct
import zlib
from pathlib import Path


def strip_metadata(source: bytes) -> bytes:
    signature = b"\x89PNG\r\n\x1a\n"
    if not source.startswith(signature):
        raise ValueError("Input is not a PNG")
    position = len(signature)
    kept = []
    kinds = []
    while position < len(source):
        if len(source) - position < 12:
            raise ValueError("Truncated PNG chunk")
        length = struct.unpack(">I", source[position : position + 4])[0]
        end = position + length + 12
        if end > len(source):
            raise ValueError("Truncated PNG payload")
        chunk = source[position:end]
        kind = chunk[4:8]
        if zlib.crc32(chunk[4:-4]) & 0xFFFFFFFF != struct.unpack(">I", chunk[-4:])[0]:
            raise ValueError("Invalid PNG checksum")
        if kind == b"IHDR":
            if length != 13 or chunk[16:21] not in (
                bytes((8, 2, 0, 0, 0)), bytes((8, 6, 0, 0, 0))
            ):
                raise ValueError("Expected a noninterlaced 8-bit RGB/RGBA PNG")
        if kind in (b"IHDR", b"IDAT", b"IEND"):
            kept.append(chunk)
            kinds.append(kind)
        elif not kind[0] & 32:
            raise ValueError("Unsupported critical PNG chunk")
        position = end
    if not kinds or kinds[0] != b"IHDR" or kinds[-1] != b"IEND":
        raise ValueError("Missing PNG header or end")
    if kinds.count(b"IHDR") != 1 or kinds.count(b"IEND") != 1 or b"IDAT" not in kinds:
        raise ValueError("Invalid PNG chunk sequence")
    return signature + b"".join(kept)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    args.destination.write_bytes(strip_metadata(args.source.read_bytes()))
