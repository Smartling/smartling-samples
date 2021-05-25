import os
import sys
import requests

API_DOMAIN = 'https://api.smartling.com'

def authenticate(user_identifier, user_secret):
    api_url = API_DOMAIN + '/auth-api/v2/authenticate'
    api_parameters = {
        'userIdentifier': user_identifier,
        'userSecret': user_secret
        }
    api_response = requests.post(api_url, json=api_parameters)
    if api_response.status_code != 200:
        raise(Exception(str(api_response.status_code) + ' ' + api_response.text))

    return api_response.json()['response']['data']['accessToken']


def get_job_progress_percent(access_token, project_id, job_uid):
    api_url = API_DOMAIN + '/jobs-api/v3/projects/' + project_id + '/jobs/' + job_uid + '/progress'
    api_request_headers = {'Authorization': 'Bearer ' + access_token}
    api_response = requests.get(api_url, headers=api_request_headers)

    if api_response.status_code != 200:
        raise(Exception(str(api_response.status_code) + ' ' + api_response.text))

    progress = api_response.json()['response']['data']['progress']
    if progress is not None:
        return progress['percentComplete']
    else:
        return 0


def main():

    # Read command-line arguments
    if len(sys.argv) != 2:
        print('Usage: status-translation-job.py <job-id>')
        sys.exit()

    job_uid = sys.argv[1]

    # Read authentication credentials from environment
    user_identifier = os.environ.get('DEV_USER_IDENTIFIER')
    user_secret = os.environ.get('DEV_USER_SECRET')
    project_id = os.environ.get('DEV_PROJECT_ID')

    if (project_id is None) or (user_identifier is None) or (user_secret is None):
        print('Missing environment variables. Did you run setenv?')
        sys.exit()

    print('Calling authentication endpoint...')
    access_token = authenticate(user_identifier, user_secret)
    print('Authenticated.')

    print('Calling "job progress" endpoint...')
    progress = get_job_progress_percent(access_token, project_id, job_uid)
    print('Job Progress: ' + str(progress) + '% complete.')

if __name__ == '__main__':
    main()
