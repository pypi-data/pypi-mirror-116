# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chuy']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['poetry = chuy:main']}

setup_kwargs = {
    'name': 'chuy',
    'version': '0.1.0',
    'description': 'Set alias to long commands.',
    'long_description': None,
    'author': 'Eliaz Bobadilla',
    'author_email': 'eliaz.bobadilladev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
