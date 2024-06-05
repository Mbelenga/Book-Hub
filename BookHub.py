#!/usr/bin/python3
"""
This module provides a function to create a .tgz archive from BookHub folder
"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """Create a tar gzipped archive of the directory BookHub."""
    # obtain the current date and time
    now = datetime.now().strftime("%Y%m%d%H%M%S")

    # Construct path where archive will be saved
    archive_path = "versions/BookHub_{}.tgz".format(now)

    # use fabric function to create directory if it doesn't exist
    local("mkdir -p versions")

    # Use tar command to create a compresses archive
    archived = local("tar -cvzf {} BookHub".format(archive_path))

    # Check archive Creation Status
    if archived.return_code != 0:
        return None
    else:
        return archive_path
