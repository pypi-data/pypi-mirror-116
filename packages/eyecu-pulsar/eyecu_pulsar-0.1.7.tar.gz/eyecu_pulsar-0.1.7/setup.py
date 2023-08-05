# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pulsar']

package_data = \
{'': ['*']}

install_requires = \
['opencv-python']

setup_kwargs = {
    'name': 'eyecu-pulsar',
    'version': '0.1.7',
    'description': 'RTSP Sync Library',
    'long_description': None,
    'author': 'Oguz Vuruskaner',
    'author_email': 'ovuruska@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eyecuvision/pulsar',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
