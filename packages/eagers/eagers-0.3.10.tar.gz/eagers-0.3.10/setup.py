# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eagers',
 'eagers.basic',
 'eagers.class_definition',
 'eagers.config',
 'eagers.forecasting',
 'eagers.plot',
 'eagers.read',
 'eagers.setup',
 'eagers.simulate',
 'eagers.solver',
 'eagers.update',
 'eagers.write']

package_data = \
{'': ['*'], 'eagers': ['demo_files/*']}

install_requires = \
['ecos>=2.0.7,<3.0.0',
 'matplotlib>=3.4.2,<4.0.0',
 'numpy>=1.21.1,<2.0.0',
 'openpyxl>=3.0.7,<4.0.0',
 'requests>=2.26.0,<3.0.0',
 'scipy>=1.7.0,<2.0.0',
 'tables>=3.6.1,<4.0.0']

extras_require = \
{'building-plus': ['building-plus>=0.1.2,<0.2.0']}

setup_kwargs = {
    'name': 'eagers',
    'version': '0.3.10',
    'description': 'Efficient Allocation of Grid Energy Resources including Storage',
    'long_description': None,
    'author': 'Dustin McLarty',
    'author_email': 'dustin.mclarty@wsu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
