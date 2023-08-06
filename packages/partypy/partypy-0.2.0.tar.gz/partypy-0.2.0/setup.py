# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['partypy']

package_data = \
{'': ['*'], 'partypy': ['data/*']}

install_requires = \
['altair-viewer>=0.3.0,<0.4.0',
 'altair>=4.1.0,<5.0.0',
 'numpy>=1.21.1,<2.0.0',
 'pandas>=1.3.1,<2.0.0']

setup_kwargs = {
    'name': 'partypy',
    'version': '0.2.0',
    'description': 'Simulate attendance at your party!',
    'long_description': '# partypy \n\n[![Python](https://img.shields.io/badge/python-3.9-blue)]()\n[![codecov](https://codecov.io/gh/TomasBeuzen/partypy/branch/main/graph/badge.svg)](https://codecov.io/gh/TomasBeuzen/partypy)\n[![Documentation Status](https://readthedocs.org/projects/partypy/badge/?version=latest)](https://partypy.readthedocs.io/en/latest/?badge=latest)\n\n\n## Installation\n\n```bash\n$ pip install -i https://test.pypi.org/simple/ partypy\n```\n\n## Features\n\n- TODO\n\n## Dependencies\n\n- TODO\n\n## Usage\n\n- TODO\n\n## Documentation\n\nThe official documentation is hosted on Read the Docs: https://partypy.readthedocs.io/en/latest/\n\n## Contributors\n\nWe welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://github.com/TomasBeuzen/partypy/graphs/contributors).\n\n### Credits\n\nThis package was created with Cookiecutter and the UBC-MDS/cookiecutter-ubc-mds project template, modified from the [pyOpenSci/cookiecutter-pyopensci](https://github.com/pyOpenSci/cookiecutter-pyopensci) project template and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage).\n',
    'author': 'Tomas Beuzen',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/TomasBeuzen/partypy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
