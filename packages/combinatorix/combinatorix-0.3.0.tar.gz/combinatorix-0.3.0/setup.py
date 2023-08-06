# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['combinatorix']
setup_kwargs = {
    'name': 'combinatorix',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Amirouche',
    'author_email': 'amirouche@hyper.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
