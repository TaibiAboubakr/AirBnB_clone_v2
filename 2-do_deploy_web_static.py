#!/usr/bin/python3
# distributes an archive to your web servers.
from fabric.api import env, put, run
import os
"""module contains do_deploy function"""
env.hosts = ['34.229.66.77', '18.209.225.222']
env.user = "ubuntu"


def do_deploy(archive_path):
    """distributes an archive to your web servers."""
    if not os.path.exists(archive_path):
        return False
    archive_name = str(archive_path).split('/')[-1]
    archive_basename = str(archive_name).split('.')[0]

    if put(archive_path, '/tmp/').failed:
        return False
    if run(f'sudo mkdir -p /data/web_static/releases/\
           {archive_basename}/').failed:
        return False
    if run(f'sudo tar -xzf /tmp/{archive_name}\
           -C /data/web_static/releases/{archive_basename}').failed:
        return False
    if run(f'sudo rm -rf /tmp/{archive_name}').failed:
        return False
    run(f"sudo mv /data/web_static/releases/{archive_basename}/web_static/*\
        /data/web_static/releases/{archive_basename}/")
    if run('sudo rm -rf /data/web_static/current').failed:
        return False
    if run('ln -sf /data/web_static/releases/{archive_basename}\
                 /data/web_static/current').failed:
        return False
    return True
