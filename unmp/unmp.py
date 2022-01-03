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
from typing import Iterator
from typing import Optional
from typing import Union

import click
import msgpack
from asserttool import eprint
from asserttool import ic
from asserttool import maxone
from asserttool import tv
from clicktool import click_add_options
from clicktool import click_global_options

signal(SIGPIPE, SIG_DFL)


def unmp(*,
         verbose: int,
         valid_types: Optional[Union[list, tuple]] = None,
         buffer_size: int = 1024,
         skip: Optional[int] = None,
         single_type: bool = True,
         ) -> Iterator[object]:
    unpacker = msgpack.Unpacker()
    index = 0
    found_type = None
    for chunk in iter(lambda: sys.stdin.buffer.read(buffer_size), b""):
        if verbose:
            #if hasattr(chunk, 'len'):
            ic(valid_types, buffer_size, type(chunk), len(chunk), chunk)
            #else:
            #    ic(valid_types, buffer_size, type(chunk), chunk)
        unpacker.feed(chunk)
        for value in unpacker:
            if single_type:
                if index == 0:
                    found_type = type(value)
                else:
                    assert isinstance(value, found_type)
            index += 1
            if verbose:
                ic(index, value)
            if skip is not None:
                if index <= skip:
                    continue
            #assert isinstance(value, list)
            if valid_types is not None:
                if type(value) not in valid_types:
                    raise TypeError('{} not in valid_types: {}'.format(type(value), valid_types))
            yield value


@click.command()
@click.option('-r', '--repr', 'use_repr', is_flag=True,)
@click.option('-h', '--hex', 'use_hex', is_flag=True,)
@click.option('--buffer', 'buffer_size', type=int, default=16384,)
@click_add_options(click_global_options)
@click.pass_context
def cli(ctx,
        buffer_size: int,
        verbose: int,
        verbose_inf: bool,
        use_repr: bool,
        use_hex: bool,
        ) -> None:

    maxone([use_repr, use_hex])

    tty, verbose = tv(ctx=ctx,
                      verbose=verbose,
                      verbose_inf=verbose_inf,
                      )
    if tty:
        if not use_repr:
            eprint('stdout is a tty, refusing to attempt to write arb py objects to it, use --repr')
            sys.stdin.close()
            sys.exit(1)

    end = b'\0'
    #if tty:
    #    end = b'\n'

    unpacker = unmp(buffer_size=buffer_size, verbose=verbose,)
    for value in unpacker:
        if verbose:
            ic(type(value), value)
        if use_repr:
            #if len(value) == 1:
            #    value = value[0]
            sys.stdout.write(repr(value) + end.decode('utf8'))
            continue
        elif use_hex:
            value = value.hex()
            sys.stdout.write(value + end.decode('utf8'))
        else:
            #if end == b'\00':  # not writing to a terminal
            # value is any py object, we need a bytes representation
            # utf8 is used, should be some locale setting, os.fsendoding thing
            # ... hm
            # if output is utf8, it's not the null terminated input stream of byte paths
            # so that's bad, unmp should fail if it cant make null terminated output, instead of trying to show a list() without --repr
            #_output = repr(value).encode('utf8')
            if verbose:
                #ic(_output)
                ic(value)
            #sys.stdout.buffer.write(_output + end)
            sys.stdout.buffer.write(value + end)  # hopefully value is bytes
            #else:
            #    assert False
            #    sys.stdout.write(value.decode('utf8') + end.decode('utf8'))
