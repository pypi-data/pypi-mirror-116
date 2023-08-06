# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_too_many', 'flake8_too_many.utils']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=3.9.2,<4.0.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.8,<0.9']}

entry_points = \
{'flake8.extension': ['TMN = flake8_too_many:Checker']}

setup_kwargs = {
    'name': 'flake8-too-many',
    'version': '0.1.0a0',
    'description': 'A flake8 plugin that prevents you from writing "too many" bad codes.',
    'long_description': None,
    'author': 'Queensferry',
    'author_email': 'queensferry.me@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
