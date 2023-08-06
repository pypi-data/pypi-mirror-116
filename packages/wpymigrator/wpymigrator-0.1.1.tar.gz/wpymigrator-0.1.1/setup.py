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
    'version': '0.1.1',
    'description': 'A program designed to aide in WordPress development site creation, and integration back into production.',
    'long_description': '# WPyMigrator\n\nA program designed to aide in WordPress development site creation, and integration back into production.\n\n---\n\n## Non-python dependencies\n\nCurrently planning to utilize WP-cli.\nThis may be removed at a later date.\nYou can verify it is installed with the following command:\n\n```bash\n$ wp --version\n# Expected output: WP-CLI x.x.x\n```\n\nIf not installed:\n```bash\n$ curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar\n$ chmod +x wp-cli.phar\n$ sudo mv wp-cli.phar /usr/local/bin/wp\n$ wp --version\n# Expected output: WP-CLI x.x.x\n```\n',
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
