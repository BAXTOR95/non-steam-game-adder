"""
config_management.py
====================

This module provides functions to load and save configuration data from/to a JSON file.

Functions
---------
load_config()
    Load the configuration from a JSON file.

save_config(config)
    Save the configuration to a JSON file.

Attributes
----------
CONFIG_FILE : str
    The name of the configuration file.

Notes
-----
- The configuration file name is set to 'config.json'.
- The `load_config` function returns an empty dictionary if the configuration file does not exist.
- The `save_config` function writes the configuration data to the file in an indented JSON format.

Example
-------
To load and save configuration data:

from config_management import load_config, save_config

config = load_config()
config['username'] = 'new_username'
save_config(config)
"""

import os
import json
import logging

CONFIG_FILE = 'config.json'


def load_config():
    """
    Load the configuration from a JSON file.

    Returns:
        dict: The configuration data loaded from the JSON file.
              If the file does not exist, an empty dictionary is returned.
    """
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as file:
                config = json.load(file)
                logging.info(f"Configuration loaded from {CONFIG_FILE}.")
                return config
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error loading configuration from {CONFIG_FILE}: {e}")
            return {}
    logging.warning(f"Configuration file {CONFIG_FILE} does not exist.")
    return {}


def save_config(config):
    """
    Save the configuration to a JSON file.

    Args:
        config (dict): The configuration data to be saved.
    """
    try:
        with open(CONFIG_FILE, 'w') as file:
            json.dump(config, file, indent=4)
            logging.info(f"Configuration saved to {CONFIG_FILE}.")
    except (TypeError, IOError) as e:
        logging.error(f"Error saving configuration to {CONFIG_FILE}: {e}")


# Configure logging
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)
