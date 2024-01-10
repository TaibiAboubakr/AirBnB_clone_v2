#!/usr/bin/python3
from fabric.api import *
from datetime import datetime
import os
"""module contains do_deploy function"""
env.hosts = ['34.229.66.77', '18.209.225.222']


@task
def do_deploy(archive_path):
    """distributes an archive to your web servers."""
    success = True
    current_directory = os.getcwd()
    full_archive_path = os.path.join(current_directory, archive_path)
    if not os.path.exists(full_archive_path):
        return False
    archive_name = str(archive_path).split('/')[-1]
    archive_basename = str(archive_path).split('/')[-1].split('.')[0]

    for host in env.hosts:
        result = put(archive_path, remote=f'/tmp/', host=host)
        success = success and result.succeeded
        result = run(f'mkdir /data/web_static/releases/{archive_basename}')
        success = success and result.succeeded
        result = run(f'tar -xzf /tmp/{archive_name}\
            -C /data/web_static/releases/{archive_basename}')
        success = success and result.succeeded
        result = run(f'rm - rf /tmp/{archive_name}')
        success = success and result.succeeded
        result = run(f'rm /data/web_static/current')
        success = success and result.succeeded
        result = run(f'ln -sf /data/web_static/releases/{archive_basename}\
                     /data/web_static/current')
    return success
