import json
import importlib.resources


def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)


def get_credentials():
    with importlib.resources.open_text("ZotTools.resources", "credentials.json") as file:
        data = json.load(file)

    return data