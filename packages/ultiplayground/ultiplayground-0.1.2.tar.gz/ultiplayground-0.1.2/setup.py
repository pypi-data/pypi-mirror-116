# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ultiplayground', 'ultiplayground.closures', 'ultiplayground.snippets']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'ultiplayground',
    'version': '0.1.2',
    'description': 'My Personal Playground',
    'long_description': '# Python Playground\n\n![CodeQL](https://github.com/UltiRequiem/python/workflows/CodeQL/badge.svg)\n![PyTest](https://github.com/UltiRequiem/python/workflows/PyTest/badge.svg)\n[![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000.svg)](https://github.com/psf/black)\n[![PyPi Version](https://img.shields.io/pypi/v/ultiplayground)](https://pypi.org/project/ultiplayground)\n![Repo Size](https://img.shields.io/github/repo-size/ultirequiem/python?style=flat-square&label=Repo)\n[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)\n![Lines of Code](https://img.shields.io/tokei/lines/github.com/UltiRequiem/python?color=blue&label=Total%20Lines)\n[![GitMoji](https://img.shields.io/badge/Gitmoji-%F0%9F%8E%A8%20-FFDD67.svg)](https://gitmoji.dev)\n\n![Cover](https://i.imgur.com/h9R7o2k.png)\n',
    'author': 'Eliaz Bobadilla',
    'author_email': 'eliaz.bobadilladev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/UltiRequiem/python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
