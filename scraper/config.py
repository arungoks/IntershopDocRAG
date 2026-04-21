"""
scraper/config.py
-----------------
Configuration loading functionality for the scraper module.
"""

from __future__ import annotations

import pathlib
from typing import Any

import yaml

def load_config(config_path: str | pathlib.Path = "config.yaml") -> dict[str, Any]:
    """Load configuration from a YAML file.

    Parameters
    ----------
    config_path:
        Path to the configuration file.

    Returns
    -------
    dict
        The parsed configuration dictionary.

    Raises
    ------
    FileNotFoundError
        If the configuration file does not exist.
    yaml.YAMLError
        If the configuration file contains invalid YAML.
    """
    path = pathlib.Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path.resolve()}")
    
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)
