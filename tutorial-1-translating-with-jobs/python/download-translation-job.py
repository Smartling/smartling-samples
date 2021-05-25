import os
import sys
import requests

API_DOMAIN = 'https://api.smartling.com'

FILE_LIST = [
    'test-files/site-navigation.json',
    'test-files/products.json'
]
LOCALE_LIST = ['fr-FR']


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


def download_translated_file(access_token,
                              project_id,
                              file_uri,
                              locale_id):

    api_url = API_DOMAIN + '/files-api/v2/projects/' + project_id + '/locales/' + locale_id + '/file'
    api_request_headers = {'Authorization': 'Bearer ' + access_token}
    api_parameters = {
        'fileUri': file_uri,
        'retrievalType' : 'published',
        'includeOriginalStrings' : False
    }
    api_response = requests.get(api_url,
                                headers=api_request_headers,
                                params=api_parameters)

    if api_response.status_code != 200:
        raise(Exception(str(api_response.status_code) + ' ' + api_response.text))

    return api_response.content


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

    print('Downloading translations...')
    for file_name in FILE_LIST:
        for locale in LOCALE_LIST:
            uri = job_uid + '/' + file_name
            content = download_translated_file(access_token, project_id, uri, locale)
            # insert locale_id before '.json' extension in translated file name
            translated_file_name = file_name[:-5] + '_' + locale + file_name[-5:]
            with open(translated_file_name, 'wb') as f:
                f.write(content)
                print('Downloaded ' + translated_file_name)


if __name__ == '__main__':
    main()
