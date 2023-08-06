# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rstream']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rstream',
    'version': '0.1.0',
    'description': 'A python client for RabbitMQ Streams',
    'long_description': None,
    'author': 'George Fortunatov',
    'author_email': 'qweeeze@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
