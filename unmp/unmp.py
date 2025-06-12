#!/usr/bin/env python3

from __future__ import annotations

import sys
from collections.abc import Iterator
from contextlib import suppress
from typing import BinaryIO
from typing import Iterator
from typing import Union
from typing import overload

import msgpack
from epprint import epprint
from globalverbose import gvd
from typing_extensions import TypeAlias
from typing_extensions import TypedDict

# Define the universe of types MessagePack can represent
MessagePackType: TypeAlias = Union[
    None,
    bool,
    int,
    float,
    str,
    bytes,
    list["MessagePackType"],
    tuple["MessagePackType", ...],
    dict["MessagePackType", "MessagePackType"],
]


@overload
def unmp(valid_types: None = ...) -> Iterator[MessagePackType]: ...
@overload
def unmp(valid_types: tuple[type[str], ...]) -> Iterator[str]: ...
@overload
def unmp(valid_types: tuple[type[bytes], ...]) -> Iterator[bytes]: ...
@overload
def unmp(valid_types: tuple[type[dict], ...]) -> Iterator[dict]: ...
@overload
def unmp(
    valid_types: tuple[type[MessagePackType], ...]
) -> Iterator[MessagePackType]: ...


def unmp(
    *,
    valid_types: tuple[type[MessagePackType], ...] | None = None,
    valid_dict_key_type: type[str] | type[bytes] | type[int] | None = None,
    valid_dict_value_type: type[str] | type[bytes] | type[int] | None = None,
    buffer_size: int = 128,
    skip: int | None = None,
    single_type: bool = True,
    strict_map_key: bool = False,
    file_handle: BinaryIO = sys.stdin.buffer,
    ignore_errors: bool = False,
    verbose: bool = False,
) -> Iterator[MessagePackType]:
    # assert verbose
    # icp(valid_types)
    # if dict in valid_types:
    #    assert valid_dict_value_type
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
                f"{valid_dict_key_type=}",
                f"{valid_dict_value_type=}",
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
