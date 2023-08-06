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
    'version': '0.1.3',
    'description': 'A python library to test services like RESTful APIs',
    'long_description': '# Welcome to the PyClinic\n\nPyclinic is a library to make it easier and faster to get your Service Testing up and running!\n\nCurrently, PyClinic can integrate with Postman users so you can export a Postman Collection and use it to automatically generate python functions!\n\nYou can also genereate Pydantic Models by using the CLI:\n\n```bash\npyclinic generate-models --input <postman_collection_path>\n```\n\n> 💡 This allows you to quickly write automation to work with many endpoints or even write automated tests against those endpoints!\n\n## Simple Example\n\n1. Export your Postman Collection (as `example.postman_collection.json`, for example)\n\n2. Make an instance of `Postman` and pass in the file path to your JSON file\n\n   ```python\n   from pyclinic.postman import Postman\n\n   runner = Postman("example.postman_collection.json")\n   ```\n\n3. Then call the endpoint function!\n\n   ```python\n   runner.Pets.list_all_pets()\n   ```\n\n## In-depth Example\n\nWhen you instantiate `Postman()`, it converts the Postman Collection JSON and turns each request to an executable function!\n\nTake this [Deck of Cards API Collection](https://github.com/ElSnoMan/pyclinic/blob/main/tests/examples/deckofcards.postman_collection.json) example. Here is what the folder structure looks like in Postman:\n\n- Root\n  - ↪️ Create shuffled deck\n  - 📂 Folder 1\n    - ↪ Reshuffle Deck\n    - 📂 Folder 1.1\n      - ↪️ Draw Cards\n  - 📂 Folder 2\n    - ↪️ List Cards in Piles\n\n1. Make an instance of Postman\n\n   ```python\n   from pyclinic.postman import Postman\n\n   runner = Postman("deckofcards.postman_collection.json")\n   ```\n\n2. To call the `Create shuffle deck` endpoint at the Collection Root, you would use\n\n   ```python\n   response = runner.Root.create_shuffled_deck()\n   ```\n\n3. Then do what you need with the Response!\n\n   > 💡 pyclinic uses the `requests` library to make requests and to work with responses!\n\n   ```python\n   assert response.ok\n   print(response.json())\n\n   """\n   Output:\n   {\n       "success": true,\n       "deck_id": "3p40paa87x90",\n       "shuffled": true,\n       "remaining": 52\n   }\n   """\n   ```\n\n4. If you want to call the `Draw Cards` item under `Folder 1 > Folder 1.1`, then use:\n\n   ```python\n   response = runner.Folder11.draw_cards()\n   ```\n\n   > 💡 All folders in the Postman Collection are flattened, so you don\'t have to do `runner.Folder1.Folder11.draw_cards()`\n\n### Normalizing Folder Names and Function Names\n\nObserve how, in the last example with `runner.Folder11.draw_cards()`, each Postman item name is turned into Pythonic syntax:\n\n- Folders are turned into classes, so `Folder 1` turns into `Folder1`\n- Requests are turned into functions, so `Draw Cards` turns into `draw_cards`\n\n### Work with them like normal functions\n\n```python\ndef test_deckofcards_multiple_calls():\n    runner = Postman("deckofcards.postman_collection.json")\n\n    create_response = runner.Root.create_shuffled_deck()\n    deck_id = create_response.json().get("deck_id")\n\n    response = runner.Folder11.draw_cards({"deck_id": deck_id})\n    assert response.ok\n    assert len(response.json()["cards"]) == 2, "Should draw two cards from deck"\n```\n\n## Setup and Contribute\n\n💡 Use `Poetry` as the package manager to take advantage of the `pyproject.toml` at the Workspace Root\n\n> ⚠️ Python version 3.9 or higher is required\n\n1. Clone/Fork this repo and open it in your favorite editor (VS Code, Pycharm, etc)\n\n2. Open the Integrated Terminal and use Poetry to install all dependencies\n\n   ```bash\n   # this also creates the virtual environment automatically\n   poetry install\n   ```\n\n3. Configure your IDE\n\n   - Select Interpreter - Gives you autocomplete, intellisense, etc\n   - Configure Tests - We use `pytest` instead of the default `unittest` library\n   - Any other settings. This project uses a Formatter (`black`) and Linter (`flake8`)\n\n4. That\'s it! Run the tests to see it all work\n\n   ```bash\n   poetry run poe test\n   ```\n\n5. Make your changes, then submit a Pull Request (PR) for review. This automatically triggers a pipeline that lints and runs tests. Once the pipeline is green, a **Maintainer** will review your PR! 😄\n\n> Shoutout to @sudomaze from Twitch 💪🏽🐍\n',
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
