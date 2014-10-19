import binascii
import urllib2
import json
from hashlib import sha1
import base64
import datetime
import calendar
import time

__author__ = 'DeStars'


class OmnitureWrapper:
    def __init__(self, user_name, secret):
        self._user_name = user_name
        self._secret = secret

    def __create_header(self):
        """
        Creates header for request
        :return: Header string
        """
        utc_timestamp = datetime.datetime.utcnow()
        nonce = str(calendar.timegm(utc_timestamp.timetuple()))
        base64nonce = binascii.b2a_base64(binascii.a2b_qp(nonce))
        created_on = utc_timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
        sha_object = sha1(nonce + created_on + self._secret)
        password_64 = base64.b64encode(bytes(sha_object.digest()))
        return 'UsernameToken Username="%s", PasswordDigest="%s", Nonce="%s", Created="%s"' % (
            self._user_name, password_64.strip(), base64nonce.strip(), created_on)

    def __get_request_data(self, request):
        request.add_header('X-WSSE', self.__create_header())
        return json.loads(urllib2.urlopen(request).read(), encoding='utf-8')

    def send_request(self, method, request_data, retry_delay=15):
        """
        Sends request to the endpoint
        :param method: String of method
        :param request_data: json object of request body
        :return: Response data
        """
        request = urllib2.Request('https://api.omniture.com/admin/1.4/rest/?method=%s' % method,
                                  json.dumps(request_data))
        try:
            return self.__get_request_data(request)
        except urllib2.HTTPError as e:
            print '{0}. Retrying in {1} seconds...'.format(e, retry_delay)
            time.sleep(retry_delay)
            return self.send_request(method, request_data)

    def retrieve_report(self, request, delay=5):
        """
        Queues and retrieves the report
        :param request: json object of request body
        :return: Report data
        """
        response = self.send_request(method='Report.Queue', request_data=request)
        time.sleep(delay)
        report = self.send_request(method='Report.Get', request_data={'reportID': response['reportID']})
        return report
