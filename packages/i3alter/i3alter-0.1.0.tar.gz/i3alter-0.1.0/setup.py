# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['i3alter']

package_data = \
{'': ['*']}

install_requires = \
['i3ipc>=2.2.1,<3.0.0', 'pynput>=1.7.3,<2.0.0']

entry_points = \
{'console_scripts': ['i3alter = i3alter.i3alter:main']}

setup_kwargs = {
    'name': 'i3alter',
    'version': '0.1.0',
    'description': 'Add alt-tab behaviour to i3',
    'long_description': None,
    'author': 'Kamyab Taghizadeh',
    'author_email': 'kamyab.zad@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
