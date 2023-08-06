# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azul']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'azul',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Cauê Baasch de Souza',
    'author_email': 'cauebs@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
