#!/usr/bin/env python3
# -*- coding: utf8 -*-

# pylint: disable=missing-docstring               # [C0111] docstrings are always outdated and wrong
# pylint: disable=missing-module-docstring        # [C0114]
# pylint: disable=fixme                           # [W0511] todo is encouraged
# pylint: disable=line-too-long                   # [C0301]
# pylint: disable=too-many-instance-attributes    # [R0902]
# pylint: disable=too-many-lines                  # [C0302] too many lines in module
# pylint: disable=invalid-name                    # [C0103] single letter var names, name too descriptive
# pylint: disable=too-many-return-statements      # [R0911]
# pylint: disable=too-many-branches               # [R0912]
# pylint: disable=too-many-statements             # [R0915]
# pylint: disable=too-many-arguments              # [R0913]
# pylint: disable=too-many-nested-blocks          # [R1702]
# pylint: disable=too-many-locals                 # [R0914]
# pylint: disable=too-few-public-methods          # [R0903]
# pylint: disable=no-member                       # [E1101] no member for base
# pylint: disable=attribute-defined-outside-init  # [W0201]
# pylint: disable=too-many-boolean-expressions    # [R0916] in if statement

from __future__ import annotations

import sys
from signal import SIG_DFL
from signal import SIGPIPE
from signal import signal

import click
from clicktool import click_add_options
from clicktool import click_global_options
from clicktool import tv
from epprint import epprint
from eprint import eprint
from mptool import unmp as _unmp

signal(SIGPIPE, SIG_DFL)


@click.command()
@click.option(
    "-r",
    "--repr",
    "use_repr",
    is_flag=True,
)
@click.option(
    "--strict-map-key",
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
    verbose: bool | int | float,
    verbose_inf: bool,
    use_repr: bool,
    dict_input: bool,
    strict_map_key: bool,
) -> None:

    assert not dict_input

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

    unpacker = _unmp(
        buffer_size=buffer_size,
        strict_map_key=strict_map_key,
        verbose=verbose,
    )
    for value in unpacker:
        if verbose:
            epprint(f"{type(value)=}", f"{value=}")
        if use_repr:
            # in this case, the values are serialized, so it's correct for human/tty use to add '\n'
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
