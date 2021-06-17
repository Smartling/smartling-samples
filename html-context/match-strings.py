import json
import os
import sys

import requests

STRINGS_FILE_URI = 'strings-test-files/strings.json'
CONTEXT_FILE_NAME = 'strings-test-files/context.html'

def main():

    # Check commandline arguments
    if len(sys.argv) != 1:
        print('No arguments required')
        sys.exit()
        
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
    print('Uploading context...')
    url = 'https://api.smartling.com/context-api/v2/projects/{0}/contexts'.format(project_id)
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

    if resp.status_code != 200:
        print(resp.status_code)
        print(resp.text)
        sys.exit()

    print('Uploaded.')
    context_uid = resp.json()['response']['data']['contextUid']

    # Download strings from the uploaded file in order to get hashcodes
    print('Getting strings from uploaded file...')
    url = 'https://api.smartling.com/strings-api/v2/projects/{0}/source-strings'.format(project_id)
    headers = {'Authorization': 'Bearer ' + access_token}
    params = {
        'fileUri': STRINGS_FILE_URI
        }
    resp = requests.get(url,
                        headers = headers,
                        params = params)

    if resp.status_code != 200:
        print(resp.status_code)
        print(resp.text)
        sys.exit()

    strings_from_uploaded_file = resp.json()['response']['data']['items']
    print('Got strings.')

    # Get the hashcodes of any strings whose keys start with 'product1'
    hashcodes_to_match = []
    for s in strings_from_uploaded_file:
        key = s['keys'][0]['key']
        if key.startswith('topic.1'):
            hashcodes_to_match.append(s['hashcode'])


    # Match context to strings within the specified set of hashcodes
    print('Initiating matching process for strings with these hashcodes...')
    print(hashcodes_to_match)
    url = 'https://api.smartling.com/context-api/v2/projects/{0}/contexts/{1}/match/async'.format(project_id, context_uid)
    headers = {'Authorization': 'Bearer ' + access_token}
    params = {
        'stringHashcodes': hashcodes_to_match
        }
    resp = requests.post(url, headers=headers, json=params)

    if resp.status_code not in [200, 202]:
        print(resp.status_code)
        print(resp.text)
        sys.exit()

    print('Context matching initiated.')



if __name__ == '__main__':
    main()
