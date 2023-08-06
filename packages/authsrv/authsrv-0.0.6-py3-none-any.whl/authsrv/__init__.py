'''
Wrapper around authsrv utilities from https://github.com/unixtools/authsrv
'''

import subprocess
import getpass

__author__ = 'Nathan Neulinger'
__url__ = 'https://github.com/unixtools/authsrv-python'
__version__ = '0.0.6'


def fetch(owner: str = None, user='', instance=''):
    '''Retrieve a stash from authsrv'''

    if owner is None:
        owner = getpass.getuser()

    password = subprocess.check_output(["authsrv-decrypt", owner, user, instance])
    password = password.decode('utf-8')
    password = password.rstrip('\n\r')

    return password
