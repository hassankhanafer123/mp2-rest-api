# data_loaders.py
from pathlib import Path

import logging
import pandas as pd
import json
import yaml


# Do not call logging.basicConfig() here.
# Use the logging configuration from Part 1.
logger = logging.getLogger(__name__)


def load_csv(filepath):
    """Load a CSV file into a DataFrame.
    filepath is a Path object.
    """
    df = pd.read_csv(filepath)
    return df


def load_json(filepath):
    """Load a JSON file into a Python object (dict or list).
    filepath is a Path object.
    """
    with open(filepath) as f: 
        data = json.load(f)
    return data


def load_yaml(filepath):
    """Load a YAML file into a Python object.
    filepath is a Path object.
    """
    with open(filepath) as f:
        data = yaml.safe_load(f)
    return data


def load_data(filepath):
    """Load a file based on its extension.
    filepath is a string, such as 'fixtures/sample.csv'
    """
    filepath = Path(filepath)
    ext = filepath.suffix.lower()
    if ext == ".csv":
        return load_csv(filepath)
    elif ext == ".json":
        return load_json(filepath)
    elif ext in [".yaml", ".yml"]:
        return load_yaml(filepath)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")