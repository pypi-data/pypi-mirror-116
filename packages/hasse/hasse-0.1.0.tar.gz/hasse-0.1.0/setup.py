# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hasse']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.2.0,<22.0.0', 'networkx>=2.6.2,<3.0.0']

setup_kwargs = {
    'name': 'hasse',
    'version': '0.1.0',
    'description': 'Python library for creating hasse diagram graphs.',
    'long_description': None,
    'author': 'Marcell Vazquez-Chanlatte',
    'author_email': 'mvc@linux.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
