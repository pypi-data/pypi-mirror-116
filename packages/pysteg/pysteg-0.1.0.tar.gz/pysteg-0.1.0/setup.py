# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pysteg']
install_requires = \
['cryptography>=3.4.7,<4.0.0', 'imageio>=2.9.0,<3.0.0']

setup_kwargs = {
    'name': 'pysteg',
    'version': '0.1.0',
    'description': 'A python library to create encrypted images using steganography.',
    'long_description': None,
    'author': 'Lior Pollak',
    'author_email': '4294489+liorp@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
