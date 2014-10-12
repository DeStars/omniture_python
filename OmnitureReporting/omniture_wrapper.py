__author__ = 'DeStars'

import binascii
import urllib2
import json
from hashlib import sha1
import base64
import datetime
import calendar


class OmnitureWrapper:
    def __init__(self, user_name, secret):
        self._user_name = user_name
        self._secret = secret

    def __create_header(self):
        utc_timestamp = datetime.datetime.utcnow()
        nonce = str(calendar.timegm(utc_timestamp.timetuple()))
        base64nonce = binascii.b2a_base64(binascii.a2b_qp(nonce))
        created_on = utc_timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
        sha_object = sha1(nonce + created_on + self._secret)
        password_64 = base64.b64encode(bytes(sha_object.digest()))
        return 'UsernameToken Username="%s", PasswordDigest="%s", Nonce="%s", Created="%s"' % (
            self._user_name, password_64.strip(), base64nonce.strip(), created_on)

    def send_request(self, method, request_data):
        request = urllib2.Request('https://api.omniture.com/admin/1.4/rest/?method=%s' % method,
                                  json.dumps(request_data))
        request.add_header('X-WSSE', self.__create_header())
        return json.loads(urllib2.urlopen(request).read(), encoding='utf-8')

    def retrieve_report(self, request):
        response = self.send_request(method='Report.Queue', request_data=request)
        report = self.send_request(method='Report.Get', request_data=response)
        return report
