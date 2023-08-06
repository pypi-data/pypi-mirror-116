# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['myhome',
 'myhome.gen',
 'myhome.gen.api',
 'myhome.gen.models',
 'myhome.gen.test',
 'myhome.object']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'nulltype>=2.3.1,<3.0.0',
 'requests>=2.25.0,<3.0.0',
 'upnpclient[autodiscovery]>=1.0.3,<2.0.0',
 'urllib3>=1.26.2,<2.0.0']

setup_kwargs = {
    'name': 'myhome',
    'version': '0.1.0',
    'description': 'Python client library for interacting with Bticino MMYHOMESERVER1',
    'long_description': None,
    'author': 'Stephan Peijnik-Steinwender',
    'author_email': 'speijnik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
