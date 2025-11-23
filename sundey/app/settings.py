import json


def load_settings(path: str = "settings.json") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data