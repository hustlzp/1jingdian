#-*- coding: UTF-8 -*-
import sys
from fabric.api import run, env, cd
sys.path.append('/var/www/flaskconfig/1jingdian')
import config

env.host_string = config.HOST_STRING


def start():
    run('supervisorctl start 1jingdian')


def restart():
    run('supervisorctl restart 1jingdian')


def deploy():
    with cd('/var/www/1jingdian'):
        run('git pull')
        run('supervisorctl restart 1jingdian')


def ldeploy():
    with cd('/var/www/1jingdian'):
        run('git pull')


def stop():
    run('supervisorctl stop 1jingdian')


def status():
    run('supervisorctl status 1jingdian')