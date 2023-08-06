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
    'version': '0.1.4',
    'description': 'A python library to test services like RESTful APIs',
    'long_description': '# Welcome to the PyClinic\n\nPyClinic is a library to make it easier and faster to get your Service Testing up and running!\n\n- [Quickstart](#quickstart)\n- [In-Depth Example](#in-depth-example)\n- [Automated Test Example](#automated-test-example)\n- [Working with Variables](#working-with-variables)\n- [Setup and Contribute](#setup-and-contribute)\n\nCurrently, PyClinic can integrate with Postman users so you can export a Postman Collection and use it to automatically generate python functions!\n\nYou can also generate Pydantic Models by using the CLI:\n\n```bash\npyclinic generate-models --input <postman_collection_path>\n```\n\n> 💡 This allows you to quickly write automation to work with many endpoints or even write automated tests against those endpoints!\n\n---\n\n## Quickstart\n\n1. Export your Collection from Postman (as `example.postman_collection.json`, for example)\n\n2. Install PyClinic with your preferred Package Manager\n\n   ```bash\n   pip install pyclinic\n   ```\n\n3. Make an instance of `Postman` and pass in the file path to your JSON file.\n\n   > 💡 You will see the instance commonly referred to as `runner`\n\n   ```python\n   from pyclinic.postman import Postman\n\n   runner = Postman("example.postman_collection.json")\n   ```\n\n4. Then call the endpoint function and do something with the response!\n\n   ```python\n   response = runner.Pets.list_all_pets()\n   assert response.ok\n   print(response.json())\n   ```\n\n---\n\n## In-Depth Example\n\nWhen you instantiate `Postman()`, it converts the Postman Collection JSON and turns each request to an executable function.\n\nTake this [Deck of Cards API Collection](https://github.com/ElSnoMan/pyclinic/blob/main/tests/examples/deckofcards.postman_collection.json) example. Here is what the folder structure looks like in Postman:\n\n- Root\n  - ↪️ Create shuffled deck\n  - 📂 Folder 1\n    - ↪ Reshuffle Deck\n    - 📂 Folder 1.1\n      - ↪️ Draw Cards\n  - 📂 Folder 2\n    - ↪️ List Cards in Piles\n\n1. Make an instance of Postman\n\n   ```python\n   from pyclinic.postman import Postman\n\n   runner = Postman("deckofcards.postman_collection.json")\n   ```\n\n2. To call the `Create shuffle deck` function at the Collection Root, you would use\n\n   ```python\n   response = runner.Root.create_shuffled_deck()\n   ```\n\n3. Then do what you need with the Response!\n\n   > 💡 pyclinic uses the `requests` library to make requests and to work with responses!\n\n   ```python\n   assert response.ok\n   print(response.json())\n\n   """ Output:\n   {\n       "success": true,\n       "deck_id": "3p40paa87x90",\n       "shuffled": true,\n       "remaining": 52\n   }\n   """\n   ```\n\n4. If you want to call the `Draw Cards` item under `Folder 1 > Folder 1.1`, then use:\n\n   ```python\n   response = runner.Folder11.draw_cards()\n   ```\n\n   > 💡 All folders in the Postman Collection are flattened, so you don\'t have to do `runner.Folder1.Folder11.draw_cards()`\n\n5. You can see all folders and functions that can be used with the `show_folders` function\n\n   ```python\n   runner.show_folders()\n   ```\n\n   ```python\n   # or use .help() to see which functions belong to a folder\n   runner.Folder1.help()\n   ```\n\n### Folder Names and Function Names are normalized\n\nObserve how, in the last example with `runner.Folder11.draw_cards()`, each Postman item name is turned into Pythonic syntax:\n\n- Folders are turned into classes, so `Folder 1` turns into `Folder1`\n- Requests are turned into functions, so `Draw Cards` turns into `draw_cards`\n\n---\n\n## Automated Test Example\n\n```python\ndef test_deckofcards_multiple_calls():\n    runner = Postman("deckofcards.postman_collection.json")\n\n    create_response = runner.Root.create_shuffled_deck()\n    deck_id = create_response.json().get("deck_id")\n\n    response = runner.Folder11.draw_cards({"deck_id": deck_id})\n    assert response.ok\n    assert len(response.json()["cards"]) == 2, "Should draw two cards from deck"\n```\n\n## Working with Variables\n\nPostman has 3 layers of Variables, but we\'ve added a 4th:\n\n1. Global\n2. Environment\n3. Collection\n4. User\n\n`Collection Variables` come as part of your collection when you export it. However, `Global` and `Environment` variables must be exported separately.\n\nWhen instantiating a Postman runner, you can pass in the paths to these exported Variables files to include them.\n\n```python\ndef test_runner_show_variables():\n   user_variables = {"USERNAME": "Carlos Kidman", "SHOW": "ME THE MONEY"}\n   runner = Postman(COLLECTION_PATH, ENV_PATH, GLOBAL_PATH, user_variables)\n   runner.show_variables()\n\n   """ Output:\n   {\n    \'NAME\': {\'value\': \'CARLOS KIDMAN\', \'enabled\': True},\n    \'BASE_URL\': {\'value\': \'https://demoqa.com\', \'enabled\': True},\n    \'USER_ID\': {\'value\': \'\', \'enabled\': True},\n    \'USERNAME\': {\'value\': \'Carlos Kidman\', \'enabled\': True},\n    \'PASSWORD\': {\'value\': \'\', \'enabled\': True},\n    \'TOKEN\': {\'value\': \'\', \'enabled\': True},\n    \'SHOW\': {\'value\': \'ME THE MONEY\', \'enabled\': True}\n   }\n   """\n```\n\n> NOTE: User Variables are defined as a flat dictionary with the key-value pairs you want. These will override values if they already exist, or add them if they don\'t\n\nFinally, you can use the `.show_variables()` method to display the variables that the Postman runner has been instantiated with.\n\n---\n\n## Setup and Contribute\n\n💡 Use `Poetry` as the package manager to take advantage of the `pyproject.toml` at the Workspace Root\n\n> ⚠️ Python version 3.9 or higher is required\n\n1. Clone/Fork this repo and open it in your favorite editor (VS Code, Pycharm, etc)\n\n2. Open the Integrated Terminal and use Poetry to install all dependencies\n\n   ```bash\n   # this also creates the virtual environment automatically\n   poetry install\n   ```\n\n3. Configure your IDE\n\n   - Select Interpreter - Gives you autocomplete, intellisense, etc\n   - Configure Tests - We use `pytest` instead of the default `unittest` library\n   - Any other settings. This project uses a Formatter (`black`) and Linter (`flake8`)\n\n4. That\'s it! Run the tests to see it all work\n\n   ```bash\n   poetry run poe test\n   ```\n\n5. Make your changes, then submit a Pull Request (PR) for review. This automatically triggers a pipeline that lints and runs tests. Once the pipeline is green, a **Maintainer** will review your PR! 😄\n\n---\n\n### Twitch Shoutouts 💪🏽🐍\n\n- **_`@sudomaze`_** - amazing feedback, humor, and searching skills\n- **_`@vernkofford`_** - OG subscriber and friend\n',
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
