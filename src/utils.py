"""Utility functions
"""

from pathlib import Path


def get_project_root() -> Path:
    """Return Path for project root directory"""
    return Path(__file__).parents[1]
