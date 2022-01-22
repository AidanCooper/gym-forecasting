"""Functions for retrieving, processing, and storing gym data
"""
# -*- coding: utf-8 -*-
import json
from typing import Dict

from dotenv import find_dotenv, load_dotenv
from src.utils import get_project_root

ROOT_DIR = get_project_root()


def get_gym_ids() -> Dict:
    """Returns dictionary with gym names as keys and ids as values"""
    with open(ROOT_DIR / "data" / "raw" / "gyms.txt", "r") as f:
        gym_ids = json.loads(f.read())
    return gym_ids


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    gym_ids = get_gym_ids()
