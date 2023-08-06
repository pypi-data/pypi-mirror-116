# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hebrew_python']

package_data = \
{'': ['*']}

install_requires = \
['friendly>=0.4.14,<0.5.0', 'ideas>=0.0.22,<0.0.23']

entry_points = \
{'console_scripts': ['hepy = hebrew_python.__main__:main']}

setup_kwargs = {
    'name': 'hebrew-python',
    'version': '0.1.0',
    'description': 'write python in Hebrew',
    'long_description': None,
    'author': 'matan h',
    'author_email': 'matan.honig2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
