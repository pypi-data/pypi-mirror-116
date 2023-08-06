# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['birtodo']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['poetry = birtodo.__main__:main']}

setup_kwargs = {
    'name': 'birtodo',
    'version': '0.1.0',
    'description': "A simple command-line interface to save user's to-dos.",
    'long_description': '<h1 align="center">BirTodo</h1>\n<p align="center">\n    ~ an extremely simple command-line interface for users to save their to-dos locally.\n</p>\n\n<h1 align="center">Some info</h1>\n<ol>\n    <li>Database: it uses the local `SQLite` database.</li>\n    <li>Features: todo add, remove, edit, show and export commands.</li>\n    <li>Documenting: every method is filled up with a corresponding docstring.</li>\n</ol>',
    'author': 'Dastan Ozgeldi',
    'author_email': 'ozgdastan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Dositan/birtodo',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
