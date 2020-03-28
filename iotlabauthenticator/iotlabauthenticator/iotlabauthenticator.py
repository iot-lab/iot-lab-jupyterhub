import os
import logging
import subprocess
from base64 import b64encode

from traitlets import Unicode

from jupyterhub.auth import Authenticator

from tornado import gen

from iotlabcli.rest import Api

USER_PATH = '/srv/jupyterhub/users/{}'


def setup_account(username, password):
    user_path = USER_PATH.format(username)
    if not os.path.exists(user_path):
        os.makedirs(user_path)

    iotlabrc_path = os.path.join(user_path, '.iotlabrc')
    enc_password = b64encode(password.encode('utf-8')).decode('utf-8')
    with open(iotlabrc_path, 'w') as f:
        f.write('{user}:{passwd}'.format(user=username, passwd=enc_password))


class IotlabAuthenticator(Authenticator):

    @gen.coroutine
    def authenticate(self, handler, data):
        _username = data['username'] 
        _password = data['password']
        api = Api(_username, _password)
        try:
            if api.check_credential():
                setup_account(_username, _password)
                return _username
        except:
            pass
        return None
