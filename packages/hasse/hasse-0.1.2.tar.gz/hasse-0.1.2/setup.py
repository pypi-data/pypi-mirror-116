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
    'version': '0.1.2',
    'description': 'Python library for representing Partially Ordered sets via Hasse Diagrams.',
    'long_description': "# hasse\nPython library for representing Partially Ordered sets via Hasse Diagrams.\n\n[![Build Status](https://cloud.drone.io/api/badges/mvcisback/hasse/status.svg)](https://cloud.drone.io/mvcisback/hasse)\n[![PyPI version](https://badge.fury.io/py/hasse.svg)](https://badge.fury.io/py/hasse)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n**Table of Contents**\n\n- [Installation](#installation)\n- [Usage](#usage)\n\n# Installation\n\nIf you just need to use `hasse`, you can just run:\n\n`$ pip install hasse`\n\nFor developers, note that this project uses the\n[poetry](https://poetry.eustace.io/) python package/dependency\nmanagement tool. Please familarize yourself with it and then\nrun:\n\n`$ poetry install`\n\n# Usage\n\n`hasse` is centered around the `hasse.PoSet` class.  An example is\ngiven below.\n\n```python\nimport hasse\n\nposet = hasse.PoSet.from_chains(\n    [1, 2, 4],  # 1 < 2 < 4\n    [1, 3, 4],  # 1 < 3 < 4\n)\n\n# Test membership and size.\nassert 2 in poset\nassert len(poset) == 4\nassert set(poset) == {1,2,3,4}\n\n# Perform pair wise comparison.\nassert poset.compare(1, 1) == '='\nassert poset.compare(1, 4) == '<'\nassert poset.compare(4, 2) == '>'\nassert poset.compare(2, 3) == '||'\n\n# Add an edge.\nposet2 = poset.add([2, 1])\nposet2.compare(1, 2) == '='\n```\n",
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
