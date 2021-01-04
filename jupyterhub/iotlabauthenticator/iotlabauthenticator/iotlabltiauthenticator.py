import os
import hashlib
import re
import requests

from requests.auth import HTTPBasicAuth

from tornado.web import MissingArgumentError

from jupyterhub.auth import Authenticator
from ltiauthenticator import LTIAuthenticator, LTILaunchValidator


JUPYTERHUB_CRYPT_KEY = os.getenv("JUPYTERHUB_CRYPT_KEY", "")
IOTLAB_ADMIN_USER = os.getenv("IOTLAB_ADMIN_USER", "")
IOTLAB_ADMIN_PASSWORD = os.getenv("IOTLAB_ADMIN_PASSWORD", "")
IOTLAB_API_URL = os.getenv("IOTLAB_API_URL", "")
if IOTLAB_API_URL == "":
    IOTLAB_API_URL = "https://www.iot-lab.info/api/"
LTI_KEY = os.getenv("LTI_KEY", "")
LTI_SECRET = os.getenv("LTI_SECRET", "")
PASSWORD_REGEXP = (
    r"^(?=.*[A-Z])"
    r"(?=.*[!@#$%^&*_=+-/])"
    r"(?=.*[0-9])"
    r"(?=.*[a-z].*[a-z].*[a-z]).{8,}"
)


class IoTLABLTIAuthenticator(LTIAuthenticator):

    consumers = {LTI_KEY:LTI_SECRET}

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

    async def authenticate(self, handler, data):
        validator = LTILaunchValidator(self.consumers)

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
            username, password = self.after_authenticate(fun_username)
            args.update(
                {
                    'userdata': {
                        'authenticator': 'mooc',
                        'username': username,
                        'password': password,
                    }
                }
            )
            return {
                'name': handler.get_body_argument('user_id'),
                'auth_state': {
                    key: value for key, value in args.items()
                    if not key.startswith('oauth_')
                }
            }
        return None

    def after_authenticate(self, username):
        # Create iot lab user in case not exists
        iot_username = IoTLABLTIAuthenticator.get_iot_user_name(username)
        iot_password = IoTLABLTIAuthenticator.get_iot_user_password(username)

        self.log.warning('Check if user %s exists' % iot_username)

        try:
            iot_auth = HTTPBasicAuth(IOTLAB_ADMIN_USER, IOTLAB_ADMIN_PASSWORD)
            url = "{}users/{}".format(IOTLAB_API_URL, iot_username)
            response = requests.get(url, auth=iot_auth)
            response.raise_for_status()
            self.log.warning('User %s exists' % iot_username)
        except requests.exceptions.RequestException as err:
            self.create_iotlab_user(iot_username, iot_password)
        return iot_username, iot_password

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
