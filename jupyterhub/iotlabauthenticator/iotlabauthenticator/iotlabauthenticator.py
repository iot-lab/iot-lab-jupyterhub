import os
import subprocess
import shlex
from base64 import b64encode

from traitlets import Unicode

from jupyterhub.auth import Authenticator

from tornado import gen

from iotlabcli.rest import Api

USERS_PATH = '/srv/jupyterhub/users'
USER_PATH = os.path.join(USERS_PATH, '{}')


@gen.coroutine
def setup_account(username, password):
    user_path = USER_PATH.format(username)

    if not os.path.exists(user_path):
        os.makedirs(user_path)

    iotlabrc_path = os.path.join(user_path, '.iotlabrc')
    if not os.path.exists(iotlabrc_path):
        enc_password = b64encode(password.encode('utf-8')).decode('utf-8')
        with open(iotlabrc_path, 'w') as f:
            f.write('{user}:{passwd}'.format(user=username,
                                             passwd=enc_password))
        cmd = "chown -R 1000:100 {}".format(iotlabrc_path)
        subprocess.call(shlex.split(cmd))

    ssh_path = os.path.join(user_path, '.ssh')
    if not os.path.exists(ssh_path):
        os.makedirs(ssh_path)

    id_rsa_path = os.path.join(ssh_path, 'id_rsa')
    if not os.path.exists(id_rsa_path):
        cmd = shlex.split('ssh-keygen -t rsa -q -N "" -C jupyterhub@iotlab -f {}'
                          .format(os.path.join(id_rsa_path)))
        subprocess.call(cmd)
        cmd = "chown -R 1000:100 {}".format(ssh_path)
        subprocess.call(shlex.split(cmd))

    training_default_path = os.path.join(USERS_PATH, '.training')
    work_path = os.path.join(user_path, 'work')
    training_path = os.path.join(work_path, 'training')
    if not os.path.exists(training_path):
        if not os.path.exists(work_path):
            os.makedirs(work_path)
        cmd = "cp -R {} {}".format(training_default_path, training_path)
        subprocess.call(shlex.split(cmd))
        cmd = "chown -R 1000:100 {}".format(work_path)
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
