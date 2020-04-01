import os
import logging
import subprocess
import shlex
from base64 import b64encode

from traitlets import Unicode

from jupyterhub.auth import Authenticator

from tornado import gen

from iotlabcli.rest import Api

USER_PATH = '/srv/jupyterhub/users/{}'


@gen.coroutine
def setup_account(username, password):
    user_path = USER_PATH.format(username)

    if not os.path.exists(user_path):
        logging.info('Creating new user directory \'%s\'', user_path)
        os.makedirs(user_path)

    iotlabrc_path = os.path.join(user_path, '.iotlabrc')
    if not os.path.exists(iotlabrc_path):
        enc_password = b64encode(password.encode('utf-8')).decode('utf-8')
        with open(iotlabrc_path, 'w') as f:
            f.write('{user}:{passwd}'.format(user=username,
                                             passwd=enc_password))

    ssh_path = os.path.join(user_path, '.ssh')
    if not os.path.exists(ssh_path):
        os.makedirs(ssh_path)

    id_rsa_path = os.path.join(ssh_path, 'id_rsa')
    if not os.path.exists(id_rsa_path):
        logging.info('Creating SSH keys for user %s', username)
        cmd = shlex.split('ssh-keygen -t rsa -q -N "" -C jupyterhub@iotlab -f {}'
                          .format(os.path.join(id_rsa_path)))
        ret = subprocess.call(cmd)
        logging.info('Result: %d', ret)

    # Force ownership of the user iotlabrc file and .ssh directory
    cmd = "chown -R 1000:100 {}".format(ssh_path)
    subprocess.call(shlex.split(cmd))
    cmd = "chown -R 1000:100 {}".format(iotlabrc_path)
    subprocess.call(shlex.split(cmd))


class IotlabAuthenticator(Authenticator):

    @gen.coroutine
    def authenticate(self, handler, data):
        _username = data['username'] 
        _password = data['password']
        api = Api(_username, _password)
        try:
            if api.check_credential():
                yield setup_account(_username, _password)
                return _username
        except:
            pass
        return None
