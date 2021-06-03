
import json
import os
import sys

import requests

def main():

    # Read command-line arguments
    if len(sys.argv) != 3:
        print('Usage: ')
        print('  Mac/Linux: python3 slupload.py <file-name> <file-type>')
        print('  Windows: py slupload.py <file-name> <file-type>')
        print('For valid file type values, see "fileType" parameter here:')
        print('https://api-reference.smartling.com/#operation/uploadSourceFile')
        sys.exit()

    file_name = sys.argv[1]
    file_type = sys.argv[2]

    # Read authentication credentials from environment
    user_id = os.environ.get('DEV_USER_IDENTIFIER')
    user_secret = os.environ.get('DEV_USER_SECRET')
    project_id = os.environ.get('DEV_PROJECT_ID')

    if (project_id is None) or (user_id is None) or (user_secret is None):
        print('Missing environment variables. Did you run setenv?')
        sys.exit()

    # Authenticate
    print('Calling authentication endpoint...')
    api_url = 'https://api.smartling.com/auth-api/v2/authenticate'
    api_parameters = {
        'userIdentifier': user_id,
        'userSecret': user_secret
        }
    api_response = requests.post(api_url, json = api_parameters)
    if api_response.status_code != 200:
        print(api_response.status_code)
        print(api_response.text)
        sys.exit()

    # Store access token for use in subsequent API calls
    access_token = api_response.json()['response']['data']['accessToken']
    print('Authenticated.')

    # Upload file to be translated
    print('Calling file upload endpoint...')
    api_url = 'https://api.smartling.com/files-api/v2/projects/' + project_id + '/file'
    api_request_headers = {'Authorization': 'Bearer ' + access_token}
    api_parameters = {
        'fileUri': file_name,
        'fileType': file_type
    }
    file_to_upload = {
        'file': open(file_name, 'rb')
    }
    api_response = requests.post(api_url,
                            headers = api_request_headers,
                            data = api_parameters,
                            files = file_to_upload)

    # Check if the upload was successful
    if api_response.status_code in [200, 202]:
        print('Uploaded ' + file_name)
    else:
        print(api_response.status_code)
        print(api_response.text)


if __name__ == '__main__':
    main()
