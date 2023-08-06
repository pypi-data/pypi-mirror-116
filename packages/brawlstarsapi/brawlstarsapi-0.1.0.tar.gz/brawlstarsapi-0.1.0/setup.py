# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['brawlstarsapi']

package_data = \
{'': ['*'], 'brawlstarsapi': ['brawlstarsapi.egg-info/*']}

setup_kwargs = {
    'name': 'brawlstarsapi',
    'version': '0.1.0',
    'description': 'Client for Brawl Stars API (https://developer.brawlstars.com/#/)',
    'long_description': None,
    'author': 'Gopher Ubunotouch',
    'author_email': 'gopherubunotouch@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
