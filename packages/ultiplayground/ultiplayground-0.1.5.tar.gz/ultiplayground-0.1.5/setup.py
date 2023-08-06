# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ultiplayground',
 'ultiplayground.closures',
 'ultiplayground.oop',
 'ultiplayground.snippets']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'ultiplayground',
    'version': '0.1.5',
    'description': 'My Personal Playground',
    'long_description': '# Python Playground\n\n![CodeQL](https://github.com/UltiRequiem/python/workflows/CodeQL/badge.svg)\n![PyTest](https://github.com/UltiRequiem/python/workflows/PyTest/badge.svg)\n![Pylint](https://github.com/UltiRequiem/python/workflows/Pylint/badge.svg)\n[![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000.svg)](https://github.com/psf/black)\n[![PyPi Version](https://img.shields.io/pypi/v/ultiplayground)](https://pypi.org/project/ultiplayground)\n![Repo Size](https://img.shields.io/github/repo-size/ultirequiem/python?style=flat-square&label=Repo)\n[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)\n![Lines of Code](https://img.shields.io/tokei/lines/github.com/UltiRequiem/python?color=blue&label=Total%20Lines)\n[![GitMoji](https://img.shields.io/badge/Gitmoji-%F0%9F%8E%A8%20-FFDD67.svg)](https://gitmoji.dev)\n![Pylint Score](https://img.shields.io/badge/Pylint%20Score-10.00-green.svg)\n\n\n![Cover](https://i.imgur.com/h9R7o2k.png)\n\nPython is an interpreted high-level general-purpose programming language.\nIt is the first programming language I learned,\nso I have quite a bit of experience with it.\n\nTo manage dependencies and build this package\nI\'m using [Poetry](https://python-poetry.org),\nand to test my functions [Pytest](https://pytest.org).\nAnd if you are curious my code\neditor is [Neovim](https://github.com/UltiRequiem/UltiVim).\n\nUsing [GitHub Actions](https://github.com/UltiRequiem/python/tree/main/.github/workflows)\nevery time that I push a commit, the project is analyzed using\n[CodeQL](https://github.com/UltiRequiem/python/blob/main/.github/workflows/codeql-analysis.yml)\nand tested with\n[PyTest](https://github.com/UltiRequiem/python/blob/main/.github/workflows/pytest.yml).\nFurthermore, every time I release a new version,\nthe package is automatically published to [PyPI](https://pypi.org/project/ultiplayground).\n\nI do some exercises and challenges every day in:\n[UltiRequiem/daily-python-practice](https://github.com/UltiRequiem/daily-python-practice)\n\n## Interesting Articles\n\n- [Python Type Checking](https://realpython.com/python-type-checking)\n- [Python\'s Instance, Class, and Static Methods Demystified](https://realpython.com/instance-class-and-static-methods-demystified)\n- [Object-Oriented Programming (OOP) in Python 3](https://realpython.com/python3-object-oriented-programming)\n- [Python Objects and Classes](https://www.programiz.com/python-programming/class)\n\n## Interesting Questions\n\n- [How can I access a classmethod from inside a class in Python](https://stackoverflow.com/questions/13900515)\n- [Should Python class filenames also be camelCased?](https://stackoverflow.com/questions/42127593)\n\n### Readed Articles\n\n- [Python Closures](https://www.programiz.com/python-programming/closure)\n- [You should know this when developing python package](https://medium.com/@udiyosovzon/things-you-should-know-when-developing-python-package-5fefc1ea3606)\n\n### Readed Questions\n\n- [How to call a function within class?](https://stackoverflow.com/questions/5615648)\n- [What is the file type of .pylintrc](https://stackoverflow.com/questions/47936144)\n- [How do I disable "missing docstring" warnings at a file-level in Pylint?](https://stackoverflow.com/questions/7877522)\n- [What\'s the meaning of the percentages displayed for each test on PyTest?](https://stackoverflow.com/questions/49738081)\n- [Python coverage badges](https://stackoverflow.com/questions/29295965)\n',
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
