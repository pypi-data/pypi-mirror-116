# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wpymigrator']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['wpym = wpymigrator.__main__:main']}

setup_kwargs = {
    'name': 'wpymigrator',
    'version': '0.1.2',
    'description': 'A program designed to aide in WordPress development site creation, and integration back into production.',
    'long_description': '# WPyMigrator\n\nThis package is still in early development.\n\n---\n',
    'author': 'Jonxslays',
    'author_email': 'jon@jonxslays.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Jonxslays/wpymigrator',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
