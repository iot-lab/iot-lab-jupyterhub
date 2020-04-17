from jupyterhub.auth import Authenticator

from tornado import gen

from iotlabcli.rest import Api


class IotlabAuthenticator(Authenticator):

    @gen.coroutine
    def authenticate(self, handler, data):
        _username = data['username']
        _password = data['password']
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
