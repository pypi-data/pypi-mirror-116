# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sisosign']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['sisosign = sisosign.sisosign:sisosign']}

setup_kwargs = {
    'name': 'sisosign',
    'version': '0.3.2',
    'description': "A command-line tool for those times when you can't decide who should go.",
    'long_description': "# sisosign\n\nFor those times when you are pair programming and the story is running longer than expected. Someone needs to go but you can't decide who should stay on the story.\n\nWhy not have a computer make these tough choices for you? **sisosign** makes it easy.\n\n## Installation\n\n```pip install sisosign```\n\nYou might need `sudo` depending on your setup.\n\n## Example usage\n\n`sisosign firstname1 firstname2`\n\nThis will print a message informing you of who should stay. Et voila! Problem solved.\n\n## Conclusion\n\nThat's it. It doesn't do anything else.\n",
    'author': 'Eric Seidler',
    'author_email': 'eric.seidler@gmail.com',
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
