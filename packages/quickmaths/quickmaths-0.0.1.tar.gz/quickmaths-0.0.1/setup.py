# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['quickmaths']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'quickmaths',
    'version': '0.0.1',
    'description': 'quick maths',
    'long_description': None,
    'author': 'jesse',
    'author_email': 'jessekrubin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dynamic-graphics-inc/dgpy-libs',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
