# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dspftwplot']

package_data = \
{'': ['*']}

install_requires = \
['dspftw', 'ipywidgets', 'matplotlib']

setup_kwargs = {
    'name': 'dspftwplot',
    'version': '2021.224.890',
    'description': 'Plotting functions for the dspftw package.',
    'long_description': '# DSPFTW Plot\n\nPlotting functions for dspftw.\n',
    'author': 'Bill Allen',
    'author_email': 'billallen256@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/dspftw/dspftwplot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
