#!/usr/bin/env python3

from __future__ import annotations

import sys
from collections.abc import Iterator
from contextlib import suppress
from typing import BinaryIO
from typing import overload

import msgpack
from epprint import epprint
from globalverbose import gvd
from typing_extensions import TypedDict


@overload
def unmp(valid_types: None) -> Iterator[str | bytes]:
    ...


@overload
def unmp(valid_types: tuple[type[str]]) -> Iterator[str]:
    ...


@overload
def unmp(valid_types: tuple[type[bytes]]) -> Iterator[bytes]:
    ...


@overload
def unmp(valid_types: tuple[type[dict]]) -> Iterator[dict]:
    ...


@overload
def unmp(valid_types: tuple[type[bytes], type[str]]) -> Iterator[str | bytes]:
    ...


@overload
def unmp(valid_types: tuple[type[str], type[bytes]]) -> Iterator[str | bytes]:
    ...


def unmp(
    *,
    # valid_types: None | tuple[type[str]] | tuple[type[bytes]] | tuple[type[str] | type[bytes]] = (str,),
    valid_types: None
    | tuple[type[str]]
    | tuple[type[bytes]]
    | tuple[type[dict]]
    | tuple[type[str], type[bytes]]
    | tuple[type[bytes], type[str]]
    | tuple[type[str], type[dict]]
    | tuple[type[dict], type[str]]
    | tuple[type[bytes], type[dict]]
    | tuple[type[dict], type[bytes]] = None,
    buffer_size: int = 128,
    skip: None | int = None,
    single_type: bool = True,
    strict_map_key: bool = False,  # True is the default
    file_handle: BinaryIO = sys.stdin.buffer,
    ignore_errors: bool = False,
    verbose: bool = False,
) -> Iterator[object]:
    assert verbose
    if verbose:
        gvd.enable()
        epprint(
            f"{valid_types=}",
            f"{buffer_size=}",
        )
    _Unpacker_Options = TypedDict(
        "_Unpacker_Options",
        {"strict_map_key": bool, "use_list": bool, "unicode_errors": str},
        total=False,
    )
    _unpacker_options: _Unpacker_Options = {
        "strict_map_key": strict_map_key,
        "use_list": False,
    }
    _suppress_exceptions = []
    if ignore_errors:
        _unpacker_options["unicode_errors"] = "ignore"
        _suppress_exceptions = [ValueError]
    # unpacker = msgpack.Unpacker(strict_map_key=strict_map_key, use_list=False)
    unpacker = msgpack.Unpacker(**_unpacker_options)
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
        with suppress(*_suppress_exceptions):
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
                if valid_types:
                    if type(value) not in valid_types:
                        raise TypeError(
                            f"{type(value)} not in valid_types: {valid_types}"
                        )
                yield value
