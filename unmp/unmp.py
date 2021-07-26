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


#import os
import sys
from signal import SIG_DFL
from signal import SIGPIPE
from signal import signal

import click
import msgpack
from asserttool import eprint
from asserttool import ic
from asserttool import nevd
from asserttool import verify

#from enumerate_input import enumerate_input
signal(SIGPIPE, SIG_DFL)


@click.command()
@click.argument("mps", type=str, nargs=-1)
@click.option('--verbose', is_flag=True)
@click.option('--debug', is_flag=True)
@click.pass_context
def cli(ctx,
        mps: tuple[str],
        verbose: bool,
        debug: bool,
        ):

    null, end, verbose, debug = nevd(ctx=ctx,
                                     printn=False,
                                     ipython=False,
                                     verbose=verbose,
                                     debug=debug,)

    #buffer_size = 1024
    buffer_size = 16384
    unpacker = msgpack.Unpacker()
    current_buffer = b''
    while True:
        current_buffer = sys.stdin.buffer.read(buffer_size)
        if len(current_buffer) == 0:
            break
        unpacker.feed(current_buffer)
        for value in unpacker:
            sys.stdout.buffer.write(value + end)
