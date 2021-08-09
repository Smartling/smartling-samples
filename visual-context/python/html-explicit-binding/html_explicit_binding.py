import json
import os
import sys

import requests

sys.path.insert(1, os.path.abspath('..')) # to allow us to load module from parent directory
from context_common import authenticate, create_job_with_files

CONTEXT_FILE_NAME = 'html-explicit-binding-context.html'
CONTENT_FILES = ['html-explicit-binding-contentfile1.json']
STRINGS_FILE_URI = CONTENT_FILES[0] # first file - will use file name as URI
JOB_NAME = 'html-explicit-binding'
LOCALE_IDS = ['fr-FR']
AUTHORIZE = True

def main():

    # Read authentication credentials from environment
    user_id = os.environ.get('DEV_USER_IDENTIFIER')
    user_secret = os.environ.get('DEV_USER_SECRET')
    project_id = os.environ.get('DEV_PROJECT_ID')

    if (project_id is None) or (user_id is None) or (user_secret is None):
        print('Missing environment variables. Did you run setenv?')
        sys.exit()

    access_token = authenticate(user_id, user_secret)

    create_job_with_files(access_token, project_id, JOB_NAME, CONTENT_FILES, LOCALE_IDS, AUTHORIZE)

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
                    'text/html')
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


    # Associate specific strings in the project with the uploaded context by 
    # creating 'bindings' between the project string (identified by hashcode) and 
    # the corresponding string in the context HTML (identified by the value of the
    # data-sl-anchor attribute).
    # It's important to use ordered integers for the data-sl-anchor values because
    # the values are used to sort the translatable content in the translation interface
    # allowing translators to work on the content in the same order as it appears in the 
    # context. 
    # For this example, the values are hard-coded in the sample context HTML and
    # a mapping between those values and the string keys is hardcoded below. In 
    # a production implementation, these values and mappings would likely be 
    # constructed on the fly as part of the process of generating the context HTML.
    key_to_anchor_mappings = {
        'topic.1.name': '0',
        'topic.1.description': '1'
        }

    bindings = []
    for s in strings_from_uploaded_files:
        key = s['keys'][0]['key']

        # Bind this context to 'topic.1' strings for this example
        if key.startswith('topic.1'): 
            bindings.append(
                {
                    'contextUid': context_uid,
                    'stringHashcode': s['hashcode'],
                    'selector': {
                        'anchors': [key_to_anchor_mappings[key]]
                    }
                }
            )

        # It's also possible to bind a project string to context without specifying
        # a specific string in the context. This causes the context to display in
        # the translation interface without any string being highlighted in it.
        # This might be appropriate when the string is not visible, such as with
        # certain HTML metadata, or perhaps if the location of the string in the 
        # context is unknown.
        elif key.startswith('meta.1'):
            bindings.append({
                    'contextUid': context_uid,
                    'stringHashcode': s['hashcode']
                    # no 'selector' node
                })

        else:
            pass # string is not associated with this context

    print('Bindings to be uploaded: ')
    print(json.dumps(bindings, indent=2))

    # Load the bindings into Smartling
    print('Uploading bindings...')
    url = 'https://api.smartling.com/context-api/v2/projects/{0}/bindings'.format(project_id)
    headers = {'Authorization': 'Bearer ' + access_token}
    payload = {'bindings': bindings}

    resp = requests.post(url, headers=headers, json=payload)

    if resp.status_code != 200:
        print(resp.status_code)
        print(resp.text)
        sys.exit()

    bindings_created = resp.json()['response']['data']['created']['totalCount']
    print('Number of bindings created: {0}'.format(bindings_created))
    print('Review results in the Dashboard')


if __name__ == '__main__':
    main()
