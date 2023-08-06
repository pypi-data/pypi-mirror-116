# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pysteg']
install_requires = \
['cryptography>=3.4.7,<4.0.0', 'imageio>=2.9.0,<3.0.0']

setup_kwargs = {
    'name': 'pysteg',
    'version': '0.1.1',
    'description': 'A python library to create encrypted images using steganography.',
    'long_description': '[![PyPI version](https://badge.fury.io/py/pysteg.svg)](https://badge.fury.io/py/pysteg)\n\n# pysteg\npysteg is a python library for image steganography.\n\nFrom Wikipedia:  \nSteganography is the practice of concealing a message within another message or a physical object.  \nIn computing/electronic contexts, a computer file, message, image, or video is concealed within another file, message, image, or video.  \nThe word steganography comes from Greek steganographia, which combines the words steganós (στεγανός), meaning "covered or concealed", and -graphia (γραφή) meaning "writing".\n\n# Usage\nPlease see usage_example.py\n\n# Dependencies\ncryptography and imageio  \nBuilt with poetry\n\n# License\nMIT',
    'author': 'Lior Pollak',
    'author_email': '4294489+liorp@users.noreply.github.com',
    'maintainer': 'Lior Pollak',
    'maintainer_email': '4294489+liorp@users.noreply.github.com',
    'url': 'https://github.com/liorp/pysteg',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
