# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vasvscrapper',
 'vasvscrapper.attendance',
 'vasvscrapper.attendance.utilities',
 'vasvscrapper.enums',
 'vasvscrapper.login',
 'vasvscrapper.login.utilities',
 'vasvscrapper.network_requests',
 'vasvscrapper.news',
 'vasvscrapper.news.utilities',
 'vasvscrapper.results',
 'vasvscrapper.results.utilities',
 'vasvscrapper.status_codes']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'bs4>=0.0.1,<0.0.2', 'lxml>=4.6.3,<5.0.0']

entry_points = \
{'console_scripts': ['lint = vasvscrapper.scripts:lint',
                     'release = vasvscrapper.scripts:release',
                     'test = vasvscrapper.scripts:test']}

setup_kwargs = {
    'name': 'vasvscrapper',
    'version': '0.0.2a8',
    'description': 'A python package for the-vasv-deets project to extract information from vce.ac.in.',
    'long_description': '# vasvscrapper\nA Scrapper for the-vasv-deets\n',
    'author': 'P. Soumith Reddy',
    'author_email': 'soumithreddypodduturi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/vasvscrapper/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
