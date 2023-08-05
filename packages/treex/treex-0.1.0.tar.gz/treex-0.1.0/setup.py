# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['treex']

package_data = \
{'': ['*']}

install_requires = \
['jax>=0.2.18,<0.3.0', 'jaxlib>=0.1.70,<0.2.0', 'optax>=0.0.9,<0.0.10']

setup_kwargs = {
    'name': 'treex',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Cristian Garcia',
    'author_email': 'cgarcia.e88@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
