# -*- coding: utf-8 -*-


from setuptools import find_packages
from setuptools import setup

import fastentrypoints

dependencies = [
    "click",
    "eprint @ git+https://git@github.com/jakeogh/epprint",
    "globalverbose @ git+https://git@github.com/jakeogh/globalverbose",
]

config = {
    "version": "0.1",
    "name": "unmp",
    "url": "https://github.com/jakeogh/unmp",
    "license": "ISC",
    "author": "Justin Keogh",
    "author_email": "github.com@v6y.net",
    "description": "Short explination of what it does _here_",
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
