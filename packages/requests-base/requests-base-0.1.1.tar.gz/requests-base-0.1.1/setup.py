# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['requests_base']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'requests-base',
    'version': '0.1.1',
    'description': '',
    'long_description': '# Requests Base\n\n[![GitHub Super-Linter](https://github.com/michaeltinsley/requests-base/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n',
    'author': 'Michael Tinsley',
    'author_email': 'michaeltinsley@outlook.com',
    'maintainer': 'Michael Tinsley',
    'maintainer_email': 'michaeltinsley@outlook.com',
    'url': 'https://github.com/michaeltinsley/requests-base/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
