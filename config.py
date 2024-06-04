"""
config.py
=========

This module is responsible for loading environment variables, specifically the Steam API key, using the `dotenv` library.

Attributes
----------
API_KEY : str
    The Steam API key loaded from the environment variables.

Functions
---------
None

Notes
-----
- Ensure that the .env file is present in the project root directory with the following entry:
    STEAM_API_KEY=your_api_key_here
- The `dotenv.load_dotenv()` function loads environment variables from a .env file into the environment.
- The `os.getenv("STEAM_API_KEY")` function retrieves the value of the STEAM_API_KEY environment variable.

Example
-------
To use the API_KEY in another module:

from config import API_KEY

if API_KEY:
    # Proceed with using the API key
    pass
else:
    # Handle the missing API key scenario
    pass
"""

import os
import dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load environment variables from a .env file
dotenv.load_dotenv()

# Retrieve the Steam API key from environment variables
API_KEY = os.getenv("STEAM_API_KEY")

if API_KEY:
    logging.info("Successfully loaded STEAM_API_KEY from environment variables.")
else:
    logging.error(
        "Failed to load STEAM_API_KEY from environment variables. Make sure it is set in the .env file."
    )

__all__ = ['API_KEY']
