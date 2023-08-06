# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tlo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tlo',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': "Il'ya Semyonov",
    'author_email': 'ilya@marshal.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
