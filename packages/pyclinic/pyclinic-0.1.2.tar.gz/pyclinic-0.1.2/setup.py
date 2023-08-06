# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyclinic', 'pyclinic.models']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=8.10.3,<9.0.0',
 'click>=8.0.1,<9.0.0',
 'datamodel-code-generator>=0.11.8,<0.12.0',
 'jsonpath-ng>=1.5.3,<2.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'pytest>=6.2.4,<7.0.0',
 'requests>=2.26.0,<3.0.0',
 'rich>=10.7.0,<11.0.0']

entry_points = \
{'console_scripts': ['pyclinic = pyclinic.cli:cli']}

setup_kwargs = {
    'name': 'pyclinic',
    'version': '0.1.2',
    'description': 'A python library to test services like RESTful APIs',
    'long_description': "# Welcome to the PyClinic\n\nA library to test services in Python\n\n## Setup and Contribute\n\n💡 Use `Poetry` as the package manager to take advantage of the `pyproject.toml` at the Workspace Root\n\n> ⚠️ Python version 3.9 or higher is required\n\n1. Clone/Fork this repo and open it in your favorite editor (VS Code, Pycharm, etc)\n\n2. Open the Integrated Terminal and use Poetry to install all dependencies\n\n   ```bash\n   # this also creates the virtual environment automatically\n   poetry install\n   ```\n\n3. Configure your IDE\n\n   - Select Interpreter - Gives you autocomplete, intellisense, etc\n   - Configure Tests - We use `pytest` instead of the default `unittest` library\n   - Any other settings. This project uses a Formatter (`black`) and Linter (`flake8`)\n\n4. That's it! Run the tests to see it all work\n\n   ```bash\n   poetry run poe test\n   ```\n\n5. Make your changes, then submit a Pull Request (PR) for review. This automatically triggers a pipeline that lints and runs tests. Once the pipeline is green, a **Maintainer** will review your PR! 😄\n\n> Shoutout to @sudomaze from Twitch 💪🏽🐍\n",
    'author': 'Carlos Kidman',
    'author_email': 'carlos@qap.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ElSnoMan/pyclinic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
