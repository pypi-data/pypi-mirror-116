# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_secrets_manager']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'boto3>=1.18.19,<2.0.0']

setup_kwargs = {
    'name': 'python-secrets-manager',
    'version': '0.1.1',
    'description': 'A wrapper around AWS Secrets Manager for pulling secrets from AWS and getting them as python variables, pivoting on stage',
    'long_description': '',
    'author': 'Alex Drozd',
    'author_email': 'drozdster@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
