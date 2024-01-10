#!/usr/bin/python3
# distributes an archive to your web servers.
from fabric.api import *
from datetime import datetime
import os
"""module contains do_deploy function"""
env.hosts = ['34.229.66.77', '18.209.225.222']
env.user = "ubuntu"


def do_pack():
    """Generate a .tgz archive from the contents of the web_static folder."""
    current_directory = os.getcwd()
    directory_path = os.path.join(current_directory, "versions")
    if not os.path.exists(directory_path):
        local("mkdir -p versions")
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    archive_name = "web_static_{}.tgz".format(timestamp)
    print(timestamp)
    archive_path = os.path.join("versions", archive_name)
    exit_status = local("tar -cvzf {} web_static/".format(archive_path))
    if exit_status.ok:
        return archive_path
    else:
        return None


def do_deploy(archive_path):
    """distributes an archive to your web servers."""
    if os.path.exists(archive_path):
        archive_name = str(archive_path).split('/')[-1]
        archive_basename = str(archive_name).split('.')[0]

        put(archive_path, '/tmp/')
        run(f'sudo mkdir -p /data/web_static/releases/\
            {archive_basename}/')
        run(f'sudo tar -xzf /tmp/{archive_name}\
            -C /data/web_static/releases/{archive_basename}')
        run(f'sudo rm -rf /tmp/{archive_name}')
        run(f"sudo mv /data/web_static/releases/{archive_basename}/web_static/*\
            /data/web_static/releases/{archive_basename}/")
        run('sudo rm -rf /data/web_static/current')
        run('ln -sf /data/web_static/releases/{archive_basename}\
                    /data/web_static/current')
        return True
    return False
