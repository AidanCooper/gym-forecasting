"""Functions for retrieving, processing, and storing gym data
"""
# -*- coding: utf-8 -*-
import json
import os
from typing import Dict

import requests
import src.exceptions as e
from bs4 import BeautifulSoup
from dotenv import find_dotenv, load_dotenv
from src.utils import get_project_root

ROOT_DIR = get_project_root()


def get_gym_ids() -> Dict:
    """Returns dictionary with gym names as keys and ids as values"""
    with open(ROOT_DIR / "data" / "raw" / "gyms.txt", "r") as f:
        gym_ids = json.loads(f.read())
    return gym_ids


def start_gym_session(username: str, password: str) -> requests.Session:
    """Opens an authenticated session at 'www.thegymgroup.com/login/'

    Parameters
    ----------
    username : str
        Your TheGym username (email)
    password : str
        Your TheGym password (PIN, 8 digits as a string, e.g. "12345678")

    Returns
    -------
    requests.Session
        A session that can be used for querying TheGym's API, whilst authenticated
    """
    session = requests.Session()
    r = session.get("https://www.thegymgroup.com/login/")
    bs = BeautifulSoup(r.text, "html.parser")
    csrf_token = bs.find("input", attrs={"id": "forgeryToken"})["value"]

    payload = {"email": username, "pin": password, "forgeryToken": csrf_token}

    s = session.post(
        "https://www.thegymgroup.com/loginpage/auth/", data=payload, cookies=r.cookies
    )
    if "Welcome" in str(BeautifulSoup(s.text, "html.parser")):
        print("Session login successful.")
    else:
        raise (e.GymLoginException())
    return session


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    gym_ids = get_gym_ids()
    gym_u = os.getenv("gym_u")
    gym_p = os.getenv("gym_p")

    sess = start_gym_session(gym_u, gym_p)
