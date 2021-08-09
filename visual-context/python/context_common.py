import json
import os
import sys
import time

import requests

def authenticate(user_id, user_secret):

    # Authenticate
    print('Authenticating...')
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

    print('Authenticated.')
    # Return access token for use in subsequent API calls
    return resp.json()['response']['data']['accessToken']


def create_job_with_files(access_token, project_id, job_name, file_list, locale_list, authorize):
    
    # Create job
    print('Creating job...')
    url = 'https://api.smartling.com/jobs-api/v3/projects/{0}/jobs'.format(project_id)
    headers = {'Authorization': 'Bearer ' + access_token}
    params = {
        'jobName': job_name
        }
    resp = requests.post(url,
                         headers=headers,
                         json=params)
    if resp.status_code == 200:
        job_uid = resp.json()['response']['data']['translationJobUid']
        print('Created job: job_uid = ' + job_uid)
    else:
        print(resp.status_code)
        print(resp.text)
        sys.exit()
 
    
    # Create job batch
    print('Creating job batch...')
    url = 'https://api.smartling.com/job-batches-api/v2/projects/{0}/batches'.format(project_id)
    headers = {'Authorization': 'Bearer ' + access_token}
    params = {
        'authorize': authorize,
        'translationJobUid': job_uid,
        'fileUris': file_list  # we're using the file names as their URIs
        }
    resp = requests.post(url,
                         headers=headers,
                         json=params)
    if resp.status_code == 200:
        batch_uid = resp.json()['response']['data']['batchUid']
        print('Created batch: batchUid = ' + batch_uid)
    else:
        print(resp.status_code)
        print(resp.text)
        sys.exit()


    # Upload test files
    print('Uploading test files to job batch...')
    url = 'https://api.smartling.com/job-batches-api/v2/projects/{0}/batches/{1}/file'.format(project_id, batch_uid)
    headers = {'Authorization': 'Bearer ' + access_token}

    for file_name in file_list:
        file_uri = file_name  # using file names as their URIs
        params = {
            'fileUri': file_uri,
            'fileType': get_file_type(file_name),
            'localeIdsToAuthorize[]': locale_list
            }
        file_param = {
            'file': open(file_name, 'rb')
            }
        resp = requests.post(url,
                             headers=headers,
                             data=params,
                             files=file_param)
        if resp.status_code == 202:
            print('Uploaded file ' + file_name)
        else:
            print(resp.status_code)
            print(resp.text)
            sys.exit()


    # Check batch was successfully processed
    print('Checking batch status...')
    url = 'https://api.smartling.com/job-batches-api/v2/projects/{0}/batches/{1}'.format(project_id, batch_uid)
    headers = {'Authorization': 'Bearer ' + access_token}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print(resp.status_code)
        print(resp.text)
        sys.exit()

    batch_status = resp.json()['response']['data']['status']

    while batch_status != 'COMPLETED':
        print('Waiting for batch to complete; status = ' + batch_status)
        time.sleep(5)
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            print(resp.status_code)
            print(resp.text)
            sys.exit()

        batch_status = resp.json()['response']['data']['status']
    
    print('Batch completed; checking each item...')

    for file in resp.json()['response']['data']['files']:
        if file['status'] != 'COMPLETED':
            print('file {0} was not processed successfully. Errors:'.format(file['fileUri']))
            print(file['errors'])
            # Note job has been created and may be under way with some of the files
            # successfully added. Might need to be cleaned up.
            sys.exit()

    print('Each item processed successfully.')


def get_file_type(filename):
    # return Smartling file type based on filename extension for a few file types
    if '.' not in filename:
        return 'unknownfiletype'
    ext = filename[filename.rindex('.')+1:]

    if ext == 'json':
        return 'json'
    elif ext == 'csv':
        return 'csv'
    elif ext == 'properties':
        return 'java_properties'
    elif ext == 'srt':
        return 'srt'
    else:
        return 'unknownfiletype'
