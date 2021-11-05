from threading import Lock
import logging
import time

import requests

from exception import ApiAuthError

AUTH_URL = 'https://api.smartling.com/auth-api/v2/authenticate'
REFRESH_URL = 'https://api.smartling.com/auth-api/v2/authenticate/refresh'
TIME_BUFFER = 10 # seconds

class Authenticator:

    def __init__(self, user_identifier, user_secret):
        self._user_identifier = user_identifier
        self._user_secret = user_secret
        self._lock = Lock()
        self._clear_data()


    def _clear_data(self):
        self._access_token = None
        self._refresh_token = None
        self._access_expires_at = None
        self._refresh_expires_at = None


    def get_access_token(self):
        if self._token_is_valid():
            return self._access_token
        else:
            return self._create_or_refresh_token()


    def _token_is_valid(self):
        if self._access_token and time.time() < self._access_expires_at:
            return True
        else:
            return False


    def _create_or_refresh_token(self):
        with self._lock:
            if self._token_is_valid():
                return self._access_token

            if self._refresh_token and time.time() < self._refresh_expires_at:
                return self._call_refresh()
            else:
                return self._call_authenticate()


    def _call_refresh(self):
        try:
            logging.debug('Refreshing token')

            r = requests.post(REFRESH_URL, json = {'refreshToken': self._refresh_token})

        except requests.exceptions.RequestException as e:
            
            logging.error('HTTP error calling {0}'.format(REFRESH_URL))
            logging.error(e)
            raise ApiAuthError('Refresh call failed. Check log for details.')

        if r.status_code == 200:
            return self._parse_response(r)

        elif r.status_code == 401:
            # shouldn't happen; try reauthenticating
            return self._call_authenticate()

        else:
            self._clear_data()
            logging.error('Error calling {0}. Status code: {1}. Response {2}'.format(REFRESH_URL,
                                                                                     r.status_code,
                                                                                     r.text))
            raise ApiAuthError('Refresh call error. Please check log for details.')


    def _call_authenticate(self):
        try:
            logging.debug('Authenticating.')

            r = requests.post(AUTH_URL, json = {'userIdentifier': self._user_identifier,
                                                'userSecret': self._user_secret})

        except requests.exceptions.RequestException as e:

            logging.error('HTTP error calling {0}'.format(AUTH_URL))
            logging.error(e)
            raise ApiAuthError('Authentication call failed. Check log for details.')


        if r.status_code == 200:
            return self._parse_response(r)

        else:
            self._clear_data()
            logging.error('Error calling {0}. Status code: {1}. Response {2}'.format(AUTH_URL,
                                                                                     r.status_code,
                                                                                     r.text))
            raise ApiAuthError('Authentication call error. Please check log for details.')


    def _parse_response(self, r):

            self._access_token = r.json()['response']['data']['accessToken']
            self._refresh_token = r.json()['response']['data']['refreshToken']
            expires_in = r.json()['response']['data']['expiresIn']
            self._access_expires_at = time.time() + expires_in - TIME_BUFFER
            refresh_expires_in = r.json()['response']['data']['refreshExpiresIn']
            self._refresh_expires_at = time.time() + refresh_expires_in - TIME_BUFFER

            return self._access_token

