#!/usr/bin/python3
# distributes an archive to your web servers.
from fabric.api import env, put, run
import os
"""module contains do_deploy function"""
env.hosts = ['34.229.66.77', '18.209.225.222']


def do_deploy(archive_path):
    """distributes an archive to your web servers."""
    if os.path.isfile(archive_path) is False:
        return False
    archive_name = str(archive_path).split('/')[-1]
    archive_basename = str(archive_name).split('.')[0]

    if put(archive_path, f'/tmp/{archive_name}').failed:
        return False
    if run(f'mkdir /data/web_static/releases/{archive_basename}/').failed:
        return False
    if run(f'tar -xzf /tmp/{archive_name}\
        -C /data/web_static/releases/{archive_basename}').failed:
        return False
    if run(f'rm - rf /tmp/{archive_name}').failed:
        return False
    if run(f'rm /data/web_static/current').failed:
        return False
    if run(f'ln -sf /data/web_static/releases/{archive_basename}\
                 /data/web_static/current')
    return True
