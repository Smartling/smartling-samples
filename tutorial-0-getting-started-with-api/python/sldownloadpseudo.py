
import json
import os
import sys

import requests

def main():

    # Read command-line arguments
    if len(sys.argv) != 3:
        print('Usage:')
        print('  Mac/Linux: python3 sldownloadpseudo.py <file-name> <locale-id>')
        print('  Windows: py sldownloadpseudo.py <file-name> <locale-id>')
        print('To see which locales are defined in your project, go to')
        print('Project Settings > Languages in the Smartling Dashboard.')
        sys.exit()

    file_name = sys.argv[1]
    locale_id = sys.argv[2]


    # Read authentication credentials from environment
    project_id = os.environ.get('DEV_PROJECT_ID')
    user_id = os.environ.get('DEV_USER_IDENTIFIER')
    user_secret = os.environ.get('DEV_USER_SECRET')

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
    api_response = requests.post(api_url, json=api_parameters)
    if api_response.status_code != 200:
        print(api_response.status_code)
        print(api_response.text)
        sys.exit()

    access_token = api_response.json()['response']['data']['accessToken']
    print('Authenticated.')


    # Download pseudotranslated file
    print('Calling download-translation endpoint...')
    api_url = 'https://api.smartling.com/files-api/v2/projects/' + project_id + '/locales/' + locale_id + '/file'
    api_request_headers = {'Authorization': 'Bearer ' + access_token}
    api_parameters = {
        'fileUri': file_name,
        'retrievalType': 'pseudo'
    }
    api_response = requests.get(api_url,
                            headers=api_request_headers,
                            params=api_parameters)

    # If successful, write the file to disk
    if api_response.status_code == 200:

        dot = file_name.rindex('.')
        translated_file_name = file_name[:dot] + '_pseudo' + file_name[dot:]
        with open(translated_file_name, 'wb') as f:
            f.write(api_response.content)

        print('Downloaded ' + translated_file_name + '.')

    else:
        print(api_response.status_code)
        print(api_response.text)


if __name__ == '__main__':
    main()
