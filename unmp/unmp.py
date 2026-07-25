#!/usr/bin/env python3

import sys
from collections.abc import Iterator
from contextlib import suppress
from typing import BinaryIO

import msgpack
from eprint import eprint
from globalverbose import gvd

type MessagePackType = (
    None
    | bool
    | int
    | float
    | str
    | bytes
    | list["MessagePackType"]
    | tuple["MessagePackType", ...]
    | dict["MessagePackType", "MessagePackType"]
)


def unmp(
    *,
    valid_types: None | tuple[type, ...] | list[type] = None,
    valid_dict_key_type: None | type[str] | type[bytes] | type[int] = None,
    valid_dict_value_type: None | type[str] | type[bytes] | type[int] = None,
    buffer_size: int = 128,
    skip: None | int = None,
    single_type: bool = True,
    strict_map_key: bool = False,
    file_handle: BinaryIO = sys.stdin.buffer,
    ignore_errors: bool = False,
    verbose: bool = False,
) -> Iterator[MessagePackType]:
    if verbose:
        gvd.enable()
        eprint(
            f"{valid_types=}",
            f"{buffer_size=}",
        )
    _unpacker_options: dict = {
        "strict_map_key": strict_map_key,
        "use_list": False,
    }
    _suppress_exceptions: list[type[BaseException]] = []
    if ignore_errors:
        _unpacker_options["unicode_errors"] = "ignore"
        _suppress_exceptions = [ValueError]
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
            eprint(
                f"{valid_types=}",
                f"{valid_dict_key_type=}",
                f"{valid_dict_value_type=}",
                f"{buffer_size=}",
                f"{type(chunk)=}",
                f"{len(chunk)=}",
                f"{chunk=}",
            )
        unpacker.feed(chunk)
        with suppress(*_suppress_exceptions):
            for value in unpacker:
                if single_type:
                    if index == 0:
                        found_type = type(value)
                    elif not isinstance(value, found_type):
                        raise TypeError(
                            f"{value=} {type(value)=} does not match {found_type=}"
                        )
                    if isinstance(value, dict):
                        for _k, _v in value.items():
                            if valid_dict_key_type:
                                if not isinstance(_k, valid_dict_key_type):
                                    raise ValueError(
                                        f"dict key: {_k} is of type {type(_k)} but must be of type {valid_dict_key_type}"
                                    )
                            if valid_dict_value_type:
                                if not isinstance(_v, valid_dict_value_type):
                                    raise ValueError(
                                        f"dict value: {_v} is of type {type(_v)} but must be of type {valid_dict_value_type}"
                                    )
                index += 1
                if gvd:
                    eprint(f"{index=}", f"{value=}")
                if skip is not None:
                    if index <= skip:
                        continue
                if valid_types:
                    if type(value) not in valid_types:
                        raise TypeError(
                            f"{type(value)} not in valid_types: {valid_types}"
                        )
                yield value
