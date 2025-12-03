import json
from pathlib import Path

def save_json(data, filepath):
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
    f.close()

def load_json(filepath):
    with open(filepath) as f:
        return json.load(f)