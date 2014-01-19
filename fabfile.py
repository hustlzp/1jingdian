# coding: utf-8
from fabric.api import run, env, cd
from jd import config

env.host_string = config.HOST_STRING


def first():
    pass


def restart():
    run('supervisorctl restart 1jingdian')


def deploy():
    with cd('/var/www/1jingdian'):
        run('git pull')
        run('supervisorctl restart 1jingdian')