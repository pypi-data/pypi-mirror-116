# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['random_quote_generator']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'kada-random-quote-generator',
    'version': '0.1.5',
    'description': 'Randomly generate programming wisdom quote.',
    'long_description': None,
    'author': 'Kada Liao',
    'author_email': 'kadaliao@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
