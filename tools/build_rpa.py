#!/usr/bin/env python3
"""Build and verify a deterministic Ren'Py RPA-3.0 translation archive."""

from __future__ import annotations

import argparse
import hashlib
import pickle
import struct
import zlib
from pathlib import Path, PurePosixPath


HEADER_SIZE = 34
KEY = 0x53534354  # "SSCT"


def source_files(root: Path) -> list[tuple[str, Path]]:
    files = [
        (path.relative_to(root).as_posix(), path)
        for path in (root / "tl").rglob("*")
        if path.is_file()
    ]
    return sorted(files)


def build(root: Path, output: Path) -> dict[str, str]:
    files = source_files(root)
    index: dict[str, list[tuple[int, int]]] = {}
    hashes: dict[str, str] = {}
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("wb") as archive:
        archive.write(b"\0" * HEADER_SIZE)
        for name, path in files:
            data = path.read_bytes()
            offset = archive.tell()
            archive.write(data)
            index[name] = [(offset ^ KEY, len(data) ^ KEY)]
            hashes[name] = hashlib.sha256(data).hexdigest()

        index_offset = archive.tell()
        # Protocol 2 is readable by old and new Ren'Py/Python releases.
        archive.write(zlib.compress(pickle.dumps(index, protocol=2), level=9))
        archive.seek(0)
        archive.write(f"RPA-3.0 {index_offset:016x} {KEY:08x}\n".encode("ascii"))

    return hashes


def read_index(archive_path: Path) -> tuple[int, dict[str, list[tuple[int, int]]]]:
    with archive_path.open("rb") as archive:
        header = archive.readline()
        parts = header.rstrip(b"\n").split()
        if len(parts) != 3 or parts[0] != b"RPA-3.0":
            raise ValueError("Not an RPA-3.0 archive")
        index_offset = int(parts[1], 16)
        key = int(parts[2], 16)
        archive.seek(index_offset)
        index = pickle.loads(zlib.decompress(archive.read()))
    return key, index


def verify(root: Path, archive_path: Path) -> None:
    expected = {name: path for name, path in source_files(root)}
    key, index = read_index(archive_path)
    if set(index) != set(expected):
        missing = sorted(set(expected) - set(index))
        extra = sorted(set(index) - set(expected))
        raise ValueError(f"Archive entries differ; missing={missing}, extra={extra}")

    with archive_path.open("rb") as archive:
        for name, path in expected.items():
            entries = index[name]
            if len(entries) != 1 or len(entries[0]) != 2:
                raise ValueError(f"Unsupported index entry for {name!r}")
            offset, length = (value ^ key for value in entries[0])
            archive.seek(offset)
            actual = archive.read(length)
            if actual != path.read_bytes():
                raise ValueError(f"Content mismatch for {name!r}")

    print(f"Verified {len(expected)} files in {archive_path} ({archive_path.stat().st_size} bytes)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path("dist/zh_hans.rpa"))
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--require-compiled", action="store_true",
                        help="Fail unless every .rpy/.rpym source has a compiled counterpart")
    args = parser.parse_args()

    root = args.root.resolve()
    output = args.output.resolve()
    if args.require_compiled:
        missing = [name for name, path in source_files(root)
                   if path.suffix in ('.rpy', '.rpym')
                   and not path.with_suffix(path.suffix + 'c').is_file()]
        if missing:
            parser.error(f"Missing compiled scripts ({len(missing)}); compile the staged game first")
    if not args.verify_only:
        hashes = build(root, output)
        print(f"Packed {len(hashes)} files into {output}")
    verify(root, output)


if __name__ == "__main__":
    main()
