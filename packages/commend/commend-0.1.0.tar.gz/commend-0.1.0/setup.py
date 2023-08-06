# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['commend']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['commend = commend.cli:main']}

setup_kwargs = {
    'name': 'commend',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': '0x4448',
    'author_email': '86135470+0x4448@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
