# coding: utf-8
from fabric.api import run, env, cd, lcd, prefix
from jd import config

host_string = config.HOST_STRING


def first():
    env.host_string = host_string
    run('apt-get update')
    run('apt-get dist-upgrade')

    with cd('/var/www/'):
        run('git clone https://github.com/hustlzp/1jingdian.git')

    # cp config file
    env.host_string = "localhost"
    run('scp /var/www/1jingdian/jd/config_remote.py %s:/var/www/1jingdian/jd/config.py'
        % host_string)

    env.host_string = host_string
    with cd('/var/www/1jingdian'):
        # mysql
        run('mysql -uroot -poptico2014 < create_db.sql')

        # virtualenv
        run('virtualenv venv')

        with prefix('source venv/bin/activate'):
            run('pip install -r requirements.txt')
            run('python manage.py syncdb')

        # nginx
        run('cp nginx.conf /etc/nginx/sites-available/1jingdian')
        run('ln -sf /etc/nginx/sites-available/1jingdian /etc/nginx/sites-enabled/')
        run('nginx -s reload')

        # supervisor
        run('cp supervisor.conf /etc/supervisor/conf.d/1jingdian.conf')
        run('supervisorctl reread')
        run('supervisorctl update')


def restart():
    env.host_string = host_string
    run('supervisorctl restart 1jingdian')


def deploy():
    env.host_string = host_string
    with cd('/var/www/1jingdian'):
        run('git pull')
        run('supervisorctl restart 1jingdian')