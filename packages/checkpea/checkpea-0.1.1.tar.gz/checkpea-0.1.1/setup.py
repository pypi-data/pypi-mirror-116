# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['checkpea']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'checkpea',
    'version': '0.1.1',
    'description': 'Checkpea tracks the state of your application.',
    'long_description': None,
    'author': 'Dani Perez',
    'author_email': 'daniel.perez@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
