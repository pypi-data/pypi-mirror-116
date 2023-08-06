# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tzar']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'pyxdg>=0.27,<0.28', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['tzar = tzar.cli:run']}

setup_kwargs = {
    'name': 'tzar',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Daniel Valenzuela',
    'author_email': 'daniel@admetricks.com',
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
