# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pycryption']
install_requires = \
['pycryptodomex>=3.10.1,<4.0.0']

setup_kwargs = {
    'name': 'pycryption',
    'version': '1.0.0',
    'description': 'Simple Library to encrypt, dycrypt in-memory bytes or text',
    'long_description': None,
    'author': 'xcodz-dot',
    'author_email': '71920621+xcodz-dot@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
