# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bookscripter']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['bookscripter = bookscripter:main']}

setup_kwargs = {
    'name': 'bookscripter',
    'version': '0.1.0',
    'description': 'Tools for grabbing books from Library Genesis (Libgen).',
    'long_description': None,
    'author': 'fitzy1293',
    'author_email': 'fitzy1293@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
