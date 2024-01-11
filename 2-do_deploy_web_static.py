#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from datetime import datetime
from fabric.api import *
import os

env.hosts = ["34.229.66.77", "18.209.225.222"]
env.user = "ubuntu"
env.password = "betty"


def do_deploy(archive_path):
    """
        Distribute archive.
    """
    if os.path.exists(archive_path):
        name = str(archive_path).split('/')[-1]
        basename = str(name).split('.')[0]
        ver_to_deploy = "/data/web_static/releases/" + basename
        tmpname = "/tmp/" + name
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(ver_to_deploy))
        run("sudo tar -xzf {} -C {}/".format(tmpname,
                                             ver_to_deploy))
        run("sudo rm {}".format(tmpname))
        run("sudo mv {}/web_static/* {}".format(ver_to_deploy,
                                                ver_to_deploy))
        run("sudo rm -rf {}/web_static/".format(ver_to_deploy))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {}/ /data/web_static/current".format(ver_to_deploy))
        print("New version deployed!")
        return True

    return False
