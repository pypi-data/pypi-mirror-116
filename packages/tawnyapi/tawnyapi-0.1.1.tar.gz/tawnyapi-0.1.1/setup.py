# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tawnyapi', 'tawnyapi.vision']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.3.1,<9.0.0', 'aiohttp>=3.7.4,<4.0.0', 'typer>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'tawnyapi',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Marco Maier',
    'author_email': 'marco.maier@tawny.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
