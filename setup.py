# -*- coding: utf-8 -*-


from setuptools import find_packages
from setuptools import setup

import fastentrypoints

dependencies = [
    "typing-extensions",
    "eprint @ git+https://git@github.com/jakeogh/eprint",
    "epprint @ git+https://git@github.com/jakeogh/epprint",
    "clicktool @ git+https://git@github.com/jakeogh/clicktool",
    "globalverbose @ git+https://git@github.com/jakeogh/globalverbose",
]

config = {
    "version": "0.1",
    "name": "unmp",
    "url": "https://github.com/jakeogh/unmp",
    "license": "ISC",
    "author": "Justin Keogh",
    "author_email": "github.com@v6y.net",
    "description": "iterates over or removes messagepacking from stdin",
    "long_description": __doc__,
    "packages": find_packages(exclude=["tests"]),
    "package_data": {"unmp": ["py.typed"]},
    "include_package_data": True,
    "zip_safe": False,
    "platforms": "any",
    "install_requires": dependencies,
    "entry_points": {
        "console_scripts": [
            "unmp=unmp.cli:cli",
        ],
    },
}

setup(**config)
