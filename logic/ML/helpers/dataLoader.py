import json


def dataLoader(filePath):
    with open(filePath, "r", encoding="utf-8") as f:
        data = json.load(f)
    X = [entry["command"] for entry in data["commands"]]
    y = [entry["label"] for entry in data["commands"]]
    return X, y
