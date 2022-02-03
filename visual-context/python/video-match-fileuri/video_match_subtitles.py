import json
import os
import sys
import time

import requests

sys.path.insert(1, os.path.abspath('..')) # to allow us to load module from parent directory
from context_common import authenticate, create_job_with_files

CONTEXT_FILE_NAME = 'video1.mp4'
CONTENT_FILE_NAME = 'video-subtitles.srt'
JOB_NAME = 'video-match-fileuri'
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

    create_job_with_files(access_token, project_id, JOB_NAME, [CONTENT_FILE_NAME], LOCALE_IDS, AUTHORIZE)

    # Upload context file
    print('Uploading context')
    url = 'https://api.smartling.com/context-api/v2/projects/{0}/contexts'.format(project_id)
    headers = {'Authorization': 'Bearer ' + access_token}
    params = {
        'name': CONTEXT_FILE_NAME
        }
    multipart_request_data = {
        'content': (CONTEXT_FILE_NAME,
                   open(CONTEXT_FILE_NAME, 'rb'),
                   'video/mp4')
        }
    resp = requests.post(url,
                        headers = headers,
                        data = params,
                        files = multipart_request_data)
    
    if resp.status_code != 200:
        print(resp.status_code)
        print(resp.text)
        sys.exit()

    print('Uploaded context file.')
    context_uid = resp.json()['response']['data']['contextUid']


    # Match context to strings in the previously uploaded content file
    print('Initiating matching process restricted by file URI...')
    url = 'https://api.smartling.com/context-api/v2/projects/{0}/contexts/{1}/match/async'.format(project_id, context_uid)
    headers = {'Authorization': 'Bearer ' + access_token}
    params = {
        'contentFileUri': CONTENT_FILE_NAME # we used the file name as the URI when uploading
        }
    resp = requests.post(url,
                        headers = headers,
                        json = params)

    if resp.status_code not in [200, 202]:
        print(resp.status_code)
        print(resp.text)
        sys.exit()

    process_uid = resp.json()['response']['data']['processUid']

    # Check matching progress
    print('Context matching process initiated; checking async process status...')
    url = 'https://api.smartling.com/context-api/v2/projects/{0}/processes/{1}'.format(project_id, process_uid)
    headers = {'Authorization': 'Bearer ' + access_token}
    resp = requests.get(url, headers = headers)
    if resp.status_code != 200:
        print(resp.status_code)
        print(resp.text)
        sys.exit()

    process_status = resp.json()['response']['data']['processState']

    while process_status != 'COMPLETED':
        print('Waiting for matching to complete; status = ' + process_status)
        time.sleep(5)
        resp = requests.get(url, headers = headers)
        if resp.status_code != 200:
            print(resp.status_code)
            print(resp.text)
            sys.exit()
        process_status = resp.json()['response']['data']['processState']

    bindings = resp.json()['response']['data']['result']['bindings']
    print('Matching completed. Number of matches: {0}. \nReview results in Dashboard.'.format(len(bindings)))



if __name__ == '__main__':
    main()


