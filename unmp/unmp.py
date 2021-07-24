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
#import sh
from signal import SIG_DFL
from signal import SIGPIPE
from signal import signal

import click
#import time
import msgpack

signal(SIGPIPE, SIG_DFL)
#from pathlib import Path
from asserttool import eprint
from asserttool import ic
from asserttool import nevd
from asserttool import validate_slice
from asserttool import verify
#from retry_on_exception import retry_on_exception
from enumerate_input import enumerate_input

#from typing import List
#from typing import Tuple
#from typing import Sequence
#from typing import Generator
#from typing import Iterable
#from typing import ByteString
#from typing import Optional
#from typing import Union


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

    buffer_size = 10
    unpacker = msgpack.Unpacker()
    current_buffer = b''
    while True:
        current_buffer = sys.stdin.buffer.read(buffer_size)
        if len(current_buffer) == 0:
            break
        unpacker.feed(current_buffer)
        for value in unpacker:
            sys.stdout.buffer.write(value + end)


    #iterator = mps

    #index = 0
    #for index, mp in enumerate_input(iterator=iterator,
    #                                 dont_decode=True,
    #                                 null=null,
    #                                 progress=False,
    #                                 skip=None,
    #                                 head=None,
    #                                 tail=None,
    #                                 debug=debug,
    #                                 verbose=verbose,):
    #    #path = Path(os.fsdecode(path))

    #    if verbose:  # or simulate:
    #        ic(index, mp)

    #    mp_un = msgpack.unpackb(mp, raw=False)
    #    if verbose:
    #        ic(mp_un)

    #    sys.stdout.buffer.write(mp_un + end)

#   #     if ipython:
#   #         import IPython; IPython.embed()

