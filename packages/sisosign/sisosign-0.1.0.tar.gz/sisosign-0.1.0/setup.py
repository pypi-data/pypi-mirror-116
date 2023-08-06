# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sisosign']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0']

setup_kwargs = {
    'name': 'sisosign',
    'version': '0.1.0',
    'description': "For those times when you can't decide who should go.",
    'long_description': None,
    'author': 'Eric Seidler',
    'author_email': 'eric.seidler@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
