# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['affine-stubs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'types-affine',
    'version': '0.1.0',
    'description': 'Types for the Affine package',
    'long_description': None,
    'author': 'Kyle Barron',
    'author_email': 'kylebarron2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kylebarron/types-affine',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
