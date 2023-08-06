# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qft']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'qft',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Scott Lawrence',
    'author_email': 'scott.lawrence-1@colorado.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
