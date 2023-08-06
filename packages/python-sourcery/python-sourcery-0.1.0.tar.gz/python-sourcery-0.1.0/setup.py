# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['sourcery']
install_requires = \
['asyncio-foundationdb>=0.10.1,<0.11.0',
 'httpx>=0.18.2,<0.19.0',
 'loguru>=0.5.3,<0.6.0',
 'ujson>=4.0.2,<5.0.0']

setup_kwargs = {
    'name': 'python-sourcery',
    'version': '0.1.0',
    'description': 'Sources is all you need.',
    'long_description': '# python-sourcery\n\nVarious extractors that generate a SQLite database (with tricks).\n\n![Time lapse of a fire trail in the wood](https://images.unsplash.com/photo-1621969876427-526f1f93c5cb?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1100&q=80)\n',
    'author': 'Amirouche',
    'author_email': 'amirouche@hyper.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
