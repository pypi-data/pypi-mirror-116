# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['isolatr']

package_data = \
{'': ['*']}

install_requires = \
['discord.py>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'isolatr',
    'version': '0.1.0',
    'description': 'Member group isolation for raid detection.',
    'long_description': None,
    'author': 'vcokltfre',
    'author_email': 'vcokltfre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vcokltfre/isolatr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
