from jupyterhub.auth import Authenticator

from tornado import gen

from iotlabcli.rest import Api


class IoTLABAuthenticator(Authenticator):

    @gen.coroutine
    def authenticate(self, handler, data):
        _username = data['username'].strip()
        _password = data['password']
        if '@' in _username:
            # Prevent use of email as login
            return None
        api = Api(_username, _password)
        try:
            if api.check_credential():
                ret = {
                    'name': _username,
                    'auth_state': {
                        'userdata': {
                            'username': _username,
                            'password': _password,
                        }
                    }
                }
                return ret
        except:
            pass
        return None
