# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chuy']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['chuy = chuy:main']}

setup_kwargs = {
    'name': 'chuy',
    'version': '0.1.2',
    'description': 'Set alias to long commands.',
    'long_description': '# Chuy\n\n![CodeQL](https://github.com/UltiRequiem/chuy/workflows/CodeQL/badge.svg)\n![PyTest](https://github.com/UltiRequiem/chuy/workflows/PyTest/badge.svg)\n![Pylint](https://github.com/UltiRequiem/chuy/workflows/Pylint/badge.svg)\n[![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000.svg)](https://github.com/psf/black)\n[![PyPi Version](https://img.shields.io/pypi/v/chuy)](https://pypi.org/project/chuy)\n![Repo Size](https://img.shields.io/github/repo-size/ultirequiem/chuy?style=flat-square&label=Repo)\n[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)\n![Lines of Code](https://img.shields.io/tokei/lines/github.com/UltiRequiem/chuy?color=blue&label=Total%20Lines)\n\n## Example configuration file\n\n```json\n{\n  "format": "poetry run black .",\n  "lint": "poetry run pylint chuy tests",\n  "test": "poetry run pytest",\n  "package": "poetry build && poetry publish"\n}\n```\n\nThis configuration must be in the [`chuy.json`](./chuy.json) file,\nwhich must be in the root of your project.\n\n## Usage\n\nAfter having defined the commands in the [chuy.json](./chuy.json) file,\nyou can now execute them as follows:\n\n```bash\nchuy format\n $ poetry run black .\n ....\n```\n\nThis varies depending on the commands you\nhave written in the [chuy file](#example-configuration-file).\n\n```bash\nchuy lint\n $ poetry run pylint chuy tests\n ....\n```\n',
    'author': 'Eliaz Bobadilla',
    'author_email': 'eliaz.bobadilladev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/UltiRequiem/chuy',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
