# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['vktools']
setup_kwargs = {
    'name': 'vktools',
    'version': '1.0.0',
    'description': 'https://github.com/Fsoky/vktools',
    'long_description': None,
    'author': 'Fsoky',
    'author_email': 'cyberuest0x12@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
