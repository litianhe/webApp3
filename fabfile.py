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
    includes = ['static', 'templates', 'transwarp', 'favicon.ico', '*.py']
    excludes = ['test', '.*', '*.pyc', '*.pyo']
    local('rm -f dist/%s' % _TAR_FILE)
    with lcd(os.path.join(os.path.abspath('.'),'www')):
        cmd = ['tar', '--dereference', '-czvf', '../dist/%s' % _TAR_FILE]
        cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
        cmd.extend(includes)
        local(' '.join(cmd))



