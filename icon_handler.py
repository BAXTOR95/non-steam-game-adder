"""
icon_handler.py
===============

This module provides a function to extract the icon from an executable file and save it as an .ico file using the `icoextract` library.

Functions
---------
extract_icon_path(executable_path)
    Extracts the icon from the specified executable file and saves it as an .ico file.

Notes
-----
- Ensure that the `icoextract` library is installed in your environment.
- The extracted icon will be saved in the same directory as the executable with the name "icon.ico".

Example
-------
To extract the icon from an executable:

from icon_handler import extract_icon_path

icon_path = extract_icon_path("path/to/executable.exe")
if icon_path:
    print(f"Icon saved at: {icon_path}")
else:
    print("Icon extraction failed.")
"""

import os
import logging
from icoextract import IconExtractor, IconExtractorError


def extract_icon_path(executable_path):
    """
    Extract the icon from an executable file and save it as an .ico file.

    Args:
        executable_path (str): The path to the executable file.

    Returns:
        str: The path to the extracted .ico file if successful, else None.

    Raises:
        IconExtractorError: If the icon extraction fails due to malformed resources or no icons available.
    """
    try:
        extractor = IconExtractor(executable_path)
        icon_file = os.path.join(os.path.dirname(executable_path), "icon.ico")
        extractor.export_icon(icon_file, num=0)
        logging.info(f"Icon extracted and saved to: {icon_file}")
        return icon_file
    except IconExtractorError as e:
        logging.error(f"Icon extraction failed: {e}")
        return None


# Configure logging
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)
