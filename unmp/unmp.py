#!/usr/bin/env python3

from __future__ import annotations

import sys
from collections.abc import Iterator
from typing import BinaryIO

import msgpack
from epprint import epprint
from globalverbose import gvd


def unmp(
    *,
    valid_types: None | list | tuple = None,
    buffer_size: int = 1024,
    skip: None | int = None,
    single_type: bool = True,
    strict_map_key: bool = False,  # True is the default
    file_handle: BinaryIO = sys.stdin.buffer,
    verbose: bool | int | float = False,
) -> Iterator[object]:
    unpacker = msgpack.Unpacker(strict_map_key=strict_map_key, use_list=False)
    index = 0
    if valid_types:
        for _type in valid_types:
            if not isinstance(_type, type):
                raise ValueError(
                    f"valid_types was passed with a non-Type member {_type=}"
                )

    found_type: type = type(None)
    for chunk in iter(lambda: file_handle.read(buffer_size), b""):
        if gvd:
            epprint(
                f"{valid_types=}",
                f"{buffer_size=}",
                f"{type(chunk)=}," f"{len(chunk)=}",
                f"{chunk=}",
            )
        unpacker.feed(chunk)
        for value in unpacker:
            if single_type:
                if index == 0:
                    found_type = type(value)
                elif not isinstance(value, found_type):
                    raise TypeError(f"{value=} does not match {found_type=}")
            index += 1
            if gvd:
                epprint(f"{index=}", f"{value=}")
            if skip is not None:
                if index <= skip:
                    continue
            if valid_types is not None:
                if type(value) not in valid_types:
                    raise TypeError(f"{type(value)} not in valid_types: {valid_types}")
            yield value


