# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_clockify', 'tap_clockify.schemas', 'tap_clockify.tests']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.7-beta.0,<22.0',
 'requests>=2.25.1,<3.0.0',
 'singer-sdk>=0.3.3,<0.4.0']

entry_points = \
{'console_scripts': ['tap-clockify = tap_clockify.tap:TapClockify.cli']}

setup_kwargs = {
    'name': 'tap-clockify',
    'version': '1.0.1',
    'description': '`tap-clockify` is a Singer tap for Clockify, built with the Meltano SDK for Singer Taps.',
    'long_description': 'None',
    'author': 'Stephen Bailey',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<3.9',
}


setup(**setup_kwargs)
