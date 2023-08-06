# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qft']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'qft',
    'version': '0.0.3',
    'description': 'Toolkit for Lattice QFT',
    'long_description': '# Toolkit for Lattice QFT\n\n## Features\n\n- HMC implemented with jax autodifferentiation\n\n',
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
