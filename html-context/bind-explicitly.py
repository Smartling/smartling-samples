import json
import os
import sys

import requests

CONTEXT_FILE_NAME = 'binding-test-files/context.html'
STRINGS_FILE_URI = 'binding-test-files/strings.json'

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

    context_uid = resp.json()['response']['data']['contextUid']
    print('Uploaded.')


    # Download strings from the uploaded file in order to get hashcodes
    print('Getting strings from uploaded file...')
    url = 'https://api.smartling.com/strings-api/v2/projects/{0}/source-strings'.format(project_id)
    headers = {'Authorization': 'Bearer ' + access_token}
    params = {
        'fileUri': STRINGS_FILE_URI
    }
    resp = requests.get(url, headers = headers, params = params)

    if resp.status_code != 200:
        print(resp.status_code)
        print(resp.text)
        sys.exit()

    strings_from_uploaded_files = resp.json()['response']['data']['items']
    print('Got strings.')


    # Create context bindings between string hashcodes and corresponding
    # data-sl-anchor values in the context file. In this example, the string
    # keys are used for the anchor values in the context file, but they don't
    # have to be: there just needs to be some way to map between the
    # data-sl-anchor values and the keys, so that the right bindings are set
    # up. The insertion of data-sl-anchor attributes into the context html
    # file can be done as part of the context file generation process.
    bindings = []
    for s in strings_from_uploaded_files:
        key = s['keys'][0]['key']
        if key.startswith('topic.1'): # restrict this context to topic.1 strings
            bindings.append({
                    'contextUid': context_uid,
                    'stringHashcode': s['hashcode'],
                    'selector': {
                        # expects that an element in the context HTML file has
                        # a data-sl-anchor tag set to the key of this string
                        'anchors': [s['keys'][0]['key']]
                    }
                })
    #print bindings

    # Bind strings to context elements explicitly
    print('Binding strings to context elements explicitly...')
    url = 'https://api.smartling.com/context-api/v2/projects/{0}/bindings'.format(project_id)
    headers = {'Authorization': 'Bearer ' + access_token}
    payload = {'bindings': bindings}

    r = requests.post(url, headers=headers, json=payload)

    if resp.status_code != 200:
        print(resp.status_code)
        print(resp.text)
        sys.exit()

    print('Binding initiated.')


if __name__ == '__main__':
    main()
