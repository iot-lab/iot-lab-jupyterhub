import os
import hashlib
import re
import requests

from requests.auth import HTTPBasicAuth

from jupyterhub.auth import Authenticator

from tornado import gen
from tornado.web import MissingArgumentError

from ltiauthenticator import LTIAuthenticator, LTILaunchValidator
from iotlabcli.rest import Api


JUPYTERHUB_CRYPT_KEY = os.getenv("JUPYTERHUB_CRYPT_KEY", "")
IOTLAB_ADMIN_USER = os.getenv("IOTLAB_ADMIN_USER", "")
IOTLAB_ADMIN_PASSWORD = os.getenv("IOTLAB_ADMIN_PASSWORD", "")
IOTLAB_API_URL = os.getenv("IOTLAB_API_URL", "")
PASSWORD_REGEXP = (
    r"^(?=.*[A-Z])"
    r"(?=.*[!@#$%^&*_=+-/])"
    r"(?=.*[0-9])"
    r"(?=.*[a-z].*[a-z].*[a-z]).{8,}"
)


class IoTLABLTIConnector:

    def __init__(self, log):
        self.log = log

    @staticmethod
    def get_iot_user_password(username):
        """Generate password based on username using hash and masterkey
        (with suffix to accomodate regex)
        """
        key = "{}{}".format(JUPYTERHUB_CRYPT_KEY, username)
        password = "{}1$aA".format(
            hashlib.sha1(key.encode('utf-8')).hexdigest()[:8]
        )
        if re.match(PASSWORD_REGEXP, password):
            return password
        else:
            return password + 'bc'

    @staticmethod
    def get_iot_user_name(username):
        return "fun{}".format(re.sub('[^A-Za-z0-9]+', '', username)[:10])

    def authenticate(self, handler, data=None, consumers=None):
        validator = LTILaunchValidator(consumers)

        args = {}
        for key, values in handler.request.body_arguments.items():
            if len(values) == 1:
                args[key] = values[0].decode()
            else:
                args[key] = [value.decode() for value in values]

        protocol = handler.request.headers['x-forwarded-proto'].split(',')[0]

        launch_url = "{}://{}{}".format(
            protocol, handler.request.host, handler.request.uri
        )

        if validator.validate_launch_request(
            launch_url,
            handler.request.headers,
            args
        ):
            try:
                fun_username = handler.get_body_argument('lis_person_sourcedid')
            except MissingArgumentError:
                fun_username = handler.get_body_argument('user_id')
            self.after_authenticate(fun_username)
            return {
                'name': handler.get_body_argument('user_id'),
                'auth_state': {
                    k: v for k, v in args.items() if not k.startswith('oauth_')
                }
            }
        return None

    def after_authenticate(self, username):
        # Create iot lab user in case not exists
        iot_username = IoTLABLTIConnector.get_iot_user_name(username)
        iot_password = IoTLABLTIConnector.get_iot_user_password(username)

        self.log.warning('Check if user %s exists' % iot_username)

        try:
            iot_auth = HTTPBasicAuth(IOTLAB_ADMIN_USER, IOTLAB_ADMIN_PASSWORD)
            url = "{}users/{}".format(IOTLAB_API_URL, iot_username)
            response = requests.get(url, auth=iot_auth)
            response.raise_for_status()
            self.log.warning('User %s exists' % iot_username)
        except requests.exceptions.RequestException as err:
            self.create_iotlab_user(iot_username, iot_password)

    def create_iotlab_user(self, iot_username, iot_password):
        self.log.warning('Creating user %s' % iot_username)
        user_data = {
            "login": iot_username,
            "firstName": iot_username,
            "lastName": iot_username,
            "email": iot_username+"@iot-lab.info",
            "country": "France",
            "organization": "FUN",
            "motivations": "FUN student",
            "city": "FUN",
            "category": "Student",
            "password": iot_password,
            "sshkeys": [""],
            "groups": ["fun-mooc"]
        }
        try:
            iot_auth = HTTPBasicAuth(IOTLAB_ADMIN_USER, IOTLAB_ADMIN_PASSWORD)
            url = "{}users?mailing-list=off".format(IOTLAB_API_URL)
            response = requests.post(url, auth=iot_auth, json=user_data)
            response.raise_for_status()
            self.log.warning('User %s created' % iot_username)
        except requests.exceptions.RequestException as err:
            self.log.error('Error creating user %s' % iot_username)
            self.log.error(err)



class IoTLABRestConnector:

    def __init__(self, log):
        self.log = log

    def authenticate(self, handler, data=None, consumers=None):
        _username = data['username'].strip()
        _password = data['password']
        if '@' in _username:
            # Prevent use of email as login
            self.log.warning('Invalid username %s' % _username)
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


class IotlabLTIAuthenticator(LTIAuthenticator):

    @gen.coroutine
    def authenticate(self, handler, data):
        ret = None
        if handler.request.uri == "/hub/lti/launch":
            connector = IoTLABLTIConnector(self.log)
            ret = connector.authenticate(handler, data, self.consumers)

        if ret is None:
            connector = IoTLABRestConnector(self.log)
            return connector.authenticate(handler, data)

        return ret
