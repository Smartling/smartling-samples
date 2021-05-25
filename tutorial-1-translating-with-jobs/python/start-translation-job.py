import os
import sys
import requests

API_DOMAIN = 'https://api.smartling.com'

FILE_LIST = [
    'test-files/site-navigation.json',
    'test-files/products.json'
]
FILE_TYPE = 'json'
LOCALE_LIST = ['fr-FR']
AUTHORIZE = False

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


def create_job(access_token, project_id, job_name):
    api_url = API_DOMAIN + '/jobs-api/v3/projects/' + project_id + '/jobs'
    api_request_headers = {'Authorization': 'Bearer ' + access_token}
    api_parameters = {
        'jobName': job_name
    }
    api_response = requests.post(api_url,
                                 headers=api_request_headers,
                                 json=api_parameters)

    if api_response.status_code != 200:
        raise(Exception(str(api_response.status_code) + ' ' + api_response.text))

    return api_response.json()['response']['data']['translationJobUid']


def create_job_batch_v2(access_token, project_id, authorize, job_uid, file_uris):
    api_url = API_DOMAIN + '/job-batches-api/v2/projects/' + project_id + '/batches'
    api_request_headers = {'Authorization': 'Bearer ' + access_token}
    api_parameters = {
        'authorize': authorize,
        'translationJobUid': job_uid,
        'fileUris': file_uris
    }
    api_response = requests.post(api_url,
                                 headers=api_request_headers,
                                 json=api_parameters)

    if api_response.status_code != 200:
        raise(Exception(str(api_response.status_code) + ' ' + api_response.text))

    return api_response.json()['response']['data']['batchUid']


def upload_file_to_batch_v2(access_token, project_id, batch_uid, file_descriptor,
                            file_uri, file_type, locale_ids_to_authorize):
    api_url = API_DOMAIN + '/job-batches-api/v2/projects/' + project_id + '/batches/' + batch_uid + '/file'
    api_request_headers = {'Authorization': 'Bearer ' + access_token}
    api_parameters = {
        'fileUri': file_uri,
        'fileType': file_type,
        'localeIdsToAuthorize[]': locale_ids_to_authorize
    }
    file_param = {
        'file': file_descriptor
    }
    api_response = requests.post(api_url,
                                 headers=api_request_headers,
                                 data=api_parameters,
                                 files=file_param)

    if api_response.status_code != 202:
        raise(Exception(str(api_response.status_code) + ' ' + api_response.text))

    return



def main():

    # Read command-line arguments
    if len(sys.argv) != 2:
        print('Usage: start-translate-files.py <job-name>')
        sys.exit()

    job_name = sys.argv[1]

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

    print('Calling "create job" endpoint...')
    job_uid = create_job(access_token, project_id, job_name)
    print('Job created. Job ID = ' + job_uid)

    print('Calling "create job batch" endpoint...')
    # include job_uid in file URI to avoid confusion during testing
    uri_list = [job_uid + '/' + file_name for file_name in FILE_LIST]
    batch_uid = create_job_batch_v2(access_token,
                                    project_id,
                                    AUTHORIZE,
                                    job_uid,
                                    uri_list)
    print('Batch created.')

    print('Adding files to batch...')
    for file_name in FILE_LIST:
        # include job_uid in file URI to avoid confusion during testing
        uri = job_uid + '/' + file_name
        with open(file_name, 'rb') as fd:
            upload_file_to_batch_v2(access_token,
                                    project_id,
                                    batch_uid,
                                    fd,
                                    uri,
                                    FILE_TYPE,
                                    LOCALE_LIST)
            print('Added file ' + file_name)



if __name__ == '__main__':
    main()
