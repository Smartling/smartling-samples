import json
import os
import sys

import requests

CONTEXT_FILE_NAME = 'uri-test-files/context.html'
CONTENT_FILE_URI = 'uri-test-files/strings2.json'

def main():
    
    # Read authentication credentials from environment
    user_id = os.environ.get('DEV_USER_IDENTIFIER')
    user_secret = os.environ.get('DEV_USER_SECRET')
    project_id = os.environ.get('DEV_PROJECT_ID')

    if (project_id is None) or (user_id is None) or (user_secret is None):
        print('Missing environment variables. Did you run setenv?')
        sys.exit()

    # Authenticate
    print('Calling authentication endpoint...')
    url = 'https://api.smartling.com/auth-api/v2/authenticate'
    params = {
        'userIdentifier': user_id,
        'userSecret': user_secret
        }
    resp = requests.post(url, json = params)
    if resp.status_code != 200:
        print(resp.status_code)
        print(resp.text)
        sys.exit()

    # Store access token for use in subsequent API calls
    access_token = resp.json()['response']['data']['accessToken']
    print('Authenticated.')


    # Upload context
    print('Uploading context')
    base_url = 'https://api.smartling.com/context-api/v2/projects/'
    url = base_url + project_id + '/contexts'
    headers = {'Authorization': 'Bearer ' + access_token}
    params = {
        'name': CONTEXT_FILE_NAME
    }
    multipart_request_data = {
        'content': (CONTEXT_FILE_NAME, 
                    open(CONTEXT_FILE_NAME, 'rb'), 
                    'text/html', 
                    {'Expires': '0'})
    }
    resp = requests.post(url,
                        headers = headers,
                        data = params,
                        files = multipart_request_data)

    if resp.status_code not in [200, 202]:
        print(resp.status_code)
        print(resp.text)
        sys.exit()

    print('Uploaded.')
    context_uid = resp.json()['response']['data']['contextUid']


    # Match context to any strings in the specified file URI
    print('Matching context restricted by file URI...')
    base_url = 'https://api.smartling.com/context-api/v2/projects/' 
    url = base_url + project_id + '/contexts/' + context_uid + '/match/async'
    headers = {'Authorization': 'Bearer ' + access_token}
    params = {
        'contentFileUri': CONTENT_FILE_URI
    }
    resp = requests.post(url,
                        headers = headers,
                        json = params)

    if resp.status_code not in [200, 202]:
        print(resp.status_code)
        print(resp.text)
        sys.exit()

    print('Context matching iniated')



if __name__ == '__main__':
    main()


