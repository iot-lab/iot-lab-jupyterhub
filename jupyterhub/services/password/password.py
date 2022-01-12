"""
Service to display user password
"""
import os
import re
import hashlib
from urllib.parse import urlparse
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.web import RequestHandler, Application, authenticated

from jupyterhub.services.auth import HubAuthenticated


class PasswordHandler(HubAuthenticated, RequestHandler):

    @staticmethod
    def _get_iot_user_password(username):
        key = os.environ['JUPYTERHUB_CRYPT_KEY'] + username
        return hashlib.sha1(key.encode('utf-8')).hexdigest()[:8] + '1$aA'

    @staticmethod
    def _get_iot_user_name(username):
        return 'fun' + re.sub('[^A-Za-z0-9]+', '', username)[:12]

    @authenticated
    def get(self):
        user = self.get_current_user()
        self.render(
            "password.html",
            username=self._get_iot_user_name(user['name']),
            password=self._get_iot_user_password(user['name'])
        )


def main():
    app = Application([
        (os.environ.get('JUPYTERHUB_SERVICE_PREFIX', '/'), PasswordHandler),
        (r'.*', PasswordHandler),
    ])

    http_server = HTTPServer(app)
    http_server.listen(10101, "0.0.0.0")

    IOLoop.current().start()


if __name__ == '__main__':
    main()
