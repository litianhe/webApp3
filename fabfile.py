####
#fabfile.py

import os,re
from datetime import datetime

# import fabric API:
from fabric.api import *

env.user = 'ubuntu'

env.sudo_user = 'root'

env.hosts = ['10.240.219.22']

db_user = 'root'
db_password = 'PASSWORD'

_TAR_FILE = 'dist-awesome.tar.gz'

def build():
    '''
    Build dist package.
    '''
    includes = ['static', 'templates', 'favicon.ico', '*.py']
    excludes = ['test', '.*', '*.pyc', '*.pyo']
    local('rm -f dist/%s' % _TAR_FILE)
    with lcd(os.path.join(os.path.abspath('.'),'www')):
        cmd = ['tar', '--dereference', '-czvf', '../dist/%s' % _TAR_FILE]
        cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
        cmd.extend(includes)
        local(' '.join(cmd))


_REMOTE_TMP_TAR = '/tmp/%s' % _TAR_FILE
_REMOTE_BASE_DIR = '/srv/awesome'

def deploy():
    newdir = 'www-%s' % datetime.now().strftime('%y-%m-%d_%H.%M.%S')
    # del existing tar file
    run('rm -f %s' % _REMOTE_TMP_TAR)
    # upload latest tar file
    put('dist/%s' % _TAR_FILE , _REMOTE_TMP_TAR )
    # create new folder
    with cd(_REMOTE_BASE_DIR):
        sudo('rm -f www')
        sudo('ln -s %s www' % newdir)
        sudo('chown www-data:www-data www')
        sudo('chown -R www-data:www-data %s', newdir)
    # reboot python service and niginx service
    with settings(warn_only=True):
        sudo('supervisorctl stop awesome')
        sudo('supervisorctl start awesome')
        sudo('/etc/init.d/nginx reload')
