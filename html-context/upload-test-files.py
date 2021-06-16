import json
import os
import sys

import requests

def main():
    # Read command-line arguments
    if len(sys.argv) != 3:
        print('Usage: python3 upload-test-files.py <directory-name> <locale_id>')
        print(' uploads JSON test files in <directory> and adds them to a job named <directory>')
        print(' <locale_id> must be for a language that exists in the test project')
        sys.exit()

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print('Directory ' + directory + ' not found.')
        sys.exit()

    test_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.json')]
    if len(test_files) == 0:
        print('No JSON files found in specified directory')
        sys.exit()

    locale_id = sys.argv[2]

    # Read authentication credentials from environment
    user_id = os.environ.get('DEV_USER_IDENTIFIER')
    user_secret = os.environ.get('DEV_USER_SECRET')
    project_id = os.environ.get('DEV_PROJECT_ID')

    if (project_id is None) or (user_id is None) or (user_secret is None):
        print('Missing environment variables. Did you run setenv?')
        sys.exit()

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

    # Store access token for use in subsequent API calls
    access_token = resp.json()['response']['data']['accessToken']
    print('Authenticated.')

    # Create job
    print('Creating job...')
    job_name = directory
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
        'authorize': True,
        'translationJobUid': job_uid,
        'fileUris': test_files
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

    for file_name in test_files:
        file_uri = file_name
        params = {
            'fileUri': file_uri,
            'fileType': 'json',
            'localeIdsToAuthorize[]': [locale_id]
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



if __name__ == '__main__':
    main()


