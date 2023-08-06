'''
Wrapper around authsrv utilities from https://github.com/unixtools/authsrv
'''

# AuthSrv_Fetch
# AuthSrv_FetchRaw
# AuthSrv_SetPathPrefix

import subprocess
import getpass

__author__ = 'nneul'


def fetch(owner: str = None, user='', instance=''):
    '''Retrieve a stash from authsrv'''

    if owner is None:
        owner = getpass.getuser()

    password = subprocess.check_output(["authsrv-decrypt", owner, user, instance])
    password = password.decode('utf-8')
    password = password.rstrip('\n\r')

    return password
