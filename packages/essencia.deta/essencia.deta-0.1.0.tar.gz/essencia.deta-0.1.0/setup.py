# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['essencia', 'essencia.deta']

package_data = \
{'': ['*']}

install_requires = \
['deta>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'essencia.deta',
    'version': '0.1.0',
    'description': 'Deta base for essencia enterprise.',
    'long_description': None,
    'author': 'arantesdv',
    'author_email': 'arantesdv@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
