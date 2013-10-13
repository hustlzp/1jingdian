from fabric.api import run, env, cd
import sys
sys.path.append('/var/www/tornconfig/1jingdian')
import config

env.host_string = config.HOST_STRING

def start():
    run('supervisor start 1jingdian')

def restart():
    run('supervisor restart 1jingdian')

def deploy():
    with cd('/var/www/xichuangzhu'):
        run('git pull')
        run('supervisor restart 1jingdian')

def ldeploy():
    with cd('/var/www/xichuangzhu'):
        run('git pull')

def stop():
    run('supervisor stop 1jingdian')

def status():
    run('supervisor status 1jingdian')