# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ncdump_rich']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'netCDF4>=1.5.7,<2.0.0', 'rich>=10.7.0,<11.0.0']

entry_points = \
{'console_scripts': ['ncdump-rich = ncdump_rich.__main__:main']}

setup_kwargs = {
    'name': 'ncdump-rich',
    'version': '0.1.0',
    'description': 'Rich NcDump',
    'long_description': "# Rich NcDump\n\n[![PyPI](https://img.shields.io/pypi/v/ncdump-rich.svg)](https://pypi.org/project/ncdump-rich/)\n[![Status](https://img.shields.io/pypi/status/ncdump-rich.svg)](https://pypi.org/project/ncdump-rich/)\n[![Python Version](https://img.shields.io/pypi/pyversions/ncdump-rich)](https://pypi.org/project/ncdump-rich)\n[![License](https://img.shields.io/pypi/l/ncdump-rich)](https://opensource.org/licenses/GPL-3.0)\n[![Read the Docs](https://img.shields.io/readthedocs/ncdump-rich/latest.svg?label=Read%20the%20Docs)](https://ncdump-rich.readthedocs.io/)\n[![Tests](https://github.com/engeir/ncdump-rich/workflows/Tests/badge.svg)](https://github.com/engeir/ncdump-rich/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/engeir/ncdump-rich/branch/main/graph/badge.svg)](https://codecov.io/gh/engeir/ncdump-rich)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n## Features\n\n- TODO\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install _Rich NcDump_ via [pip](https://pip.pypa.io/) from [PyPI](https://pypi.org/):\n\n```sh\npip install ncdump-rich\n```\n\n## Usage\n\nPlease see the [Command-line Reference](https://ncdump-rich.readthedocs.io/en/latest/usage.html) for details.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide](CONTRIBUTING.rst).\n\n## License\n\nDistributed under the terms of the [GPL 3.0 license](https://opensource.org/licenses/GPL-3.0),\n_Rich NcDump_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue](https://github.com/engeir/ncdump-rich/issues) along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz](https://github.com/cjolowicz)'s [Hypermodern Python Cookiecutter](https://github.com/cjolowicz/cookiecutter-hypermodern-python) template.\n",
    'author': 'Eirik Enger',
    'author_email': 'eirroleng@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/engeir/ncdump-rich',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
