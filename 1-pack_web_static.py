#!/usr/bin/python3
from invoke import task
from fabric import Connection
from datetime import datetime
import os
"""module contains do_pack function"""


@task
def do_pack(c):
    """Generate a .tgz archive from the contents of the web_static folder."""
    current_directory = os.getcwd()
    directory_path = os.path.join(current_directory, "versions")
    if not os.path.exists(directory_path):
        c.run("mkdir -p versions")
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    archive_name = "web_static_{}.tgz".format(timestamp)
    print(timestamp)
    archive_path = os.path.join("versions", archive_name)
    exit_status = c.run("tar -cvzf {} web_static/".format(archive_path))
    if exit_status.ok:
        return archive_path
    else:
        return None
