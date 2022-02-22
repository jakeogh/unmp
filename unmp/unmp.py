#!/usr/bin/env python3
# -*- coding: utf8 -*-

# flake8: noqa           # flake8 has no per file settings :(
# pylint: disable=C0111  # docstrings are always outdated and wrong
# pylint: disable=C0114  #      Missing module docstring (missing-module-docstring)
# pylint: disable=W0511  # todo is encouraged
# pylint: disable=C0301  # line too long
# pylint: disable=R0902  # too many instance attributes
# pylint: disable=C0302  # too many lines in module
# pylint: disable=C0103  # single letter var names, func name too descriptive
# pylint: disable=R0911  # too many return statements
# pylint: disable=R0912  # too many branches
# pylint: disable=R0915  # too many statements
# pylint: disable=R0913  # too many arguments
# pylint: disable=R1702  # too many nested blocks
# pylint: disable=R0914  # too many local variables
# pylint: disable=R0903  # too few public methods
# pylint: disable=E1101  # no member for base
# pylint: disable=W0201  # attribute defined outside __init__
# pylint: disable=R0916  # Too many boolean expressions in if statement
# pylint: disable=C0305  # Trailing newlines editor should fix automatically, pointless warning


import sys
from math import inf
from signal import SIG_DFL
from signal import SIGPIPE
from signal import signal
from typing import Union

import click
from asserttool import maxone
from clicktool import click_add_options
from clicktool import click_global_options
from clicktool import tv
from epprint import epprint
from eprint import eprint
from mptool import unmp

signal(SIGPIPE, SIG_DFL)


@click.command()
@click.option(
    "-r",
    "--repr",
    "use_repr",
    is_flag=True,
)
@click.option(
    "-h",
    "--hex",
    "use_hex",
    is_flag=True,
)
@click.option(
    "--buffer",
    "buffer_size",
    type=int,
    default=16384,
)
@click_add_options(click_global_options)
@click.pass_context
def cli(
    ctx,
    buffer_size: int,
    verbose: Union[bool, int, float],
    verbose_inf: bool,
    use_repr: bool,
    use_hex: bool,
    dict_input: bool,
) -> None:

    assert not dict_input
    maxone([use_repr, use_hex])

    tty, verbose = tv(
        ctx=ctx,
        verbose=verbose,
        verbose_inf=verbose_inf,
    )
    if tty:
        if not use_repr:
            eprint(
                "stdout is a tty, refusing to attempt to write arb py objects to it, use --repr"
            )
            sys.stdin.close()
            sys.exit(1)

    unpacker = unmp(
        buffer_size=buffer_size,
        verbose=verbose,
    )
    for value in unpacker:
        if verbose:
            epprint(f"{type(value)=}", f"{value=}")
        if use_repr:
            # in this case, the values are serialized, so it's correct for human/tty use to add '\n'
            sys.stdout.write(repr(value) + "\n")
            continue
        if use_hex:
            value = value.hex()
            sys.stdout.write(value + "\0")
            continue

        if isinstance(value, bytes):
            sys.stdout.buffer.write(value + b"\0")  # hopefully value is bytes
            sys.stdout.buffer.flush()
        elif isinstance(value, str):
            sys.stdout.write(value + "\0")
            sys.stdout.flush()
        else:
            raise NotImplementedError
