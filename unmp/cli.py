#!/usr/bin/env python3
# -*- coding: utf8 -*-
from __future__ import annotations

import argparse
import sys
from signal import SIG_DFL
from signal import SIGPIPE
from signal import signal

from eprint import eprint

from unmp import unmp

signal(SIGPIPE, SIG_DFL)


def cli(
    buffer_size: int,
    use_repr: bool,
    strict_map_key: bool,
) -> None:
    if sys.stdout.isatty():
        if not use_repr:
            eprint(
                "stdout is a tty, refusing to attempt to write arb py objects to it, use --repr"
            )
            sys.stdin.close()
            sys.exit(1)
    unpacker = unmp(
        buffer_size=buffer_size,
        strict_map_key=strict_map_key,
    )
    for value in unpacker:
        if use_repr:
            sys.stdout.write(repr(value) + "\n")
            sys.stdout.flush()
            continue
        if isinstance(value, bytes):
            sys.stdout.buffer.write(value)
            sys.stdout.buffer.flush()
        elif isinstance(value, str):
            sys.stdout.write(value)
            sys.stdout.flush()
        else:
            raise NotImplementedError(type(value))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r",
        "--repr",
        dest="use_repr",
        action="store_true",
    )
    parser.add_argument(
        "--strict-map-key",
        action="store_true",
    )
    parser.add_argument(
        "--buffer",
        dest="buffer_size",
        type=int,
        default=16384,
    )
    args = parser.parse_args()

    cli(
        buffer_size=args.buffer_size,
        use_repr=args.use_repr,
        strict_map_key=args.strict_map_key,
    )
