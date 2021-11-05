#!/usr/bin/python3

import json
import logging
import os
import sys
import time

import requests

import auth
import exception

MAX_RETRIES = 10


def get_files_one_page(offset, limit, project_id, authenticator):

    api_url = 'https://api.smartling.com/files-api/v2/projects/{0}/files/list'.format(project_id)
    params = {
        'orderBy': 'created_asc',
        'offset': offset,
        'limit': limit
    }

    # loop to handle retries if Smartling rate limiting encountered
    for attempt in range(MAX_RETRIES):

        try:
            # get access token inside retry loop in case it expires during retry attempts
            headers = {'Authorization': 'Bearer ' + authenticator.get_access_token()}

            resp = requests.get(api_url, headers = headers, params = params)

        # (should really check for specific exceptions here in case some can be handled)
        except requests.exceptions.RequestException as e:
            logging.error('HTTP error calling {0}'.format(api_url))
            logging.error(e)
            raise exception.ApiError('Call to get files failed. Check the log for details.')


        if resp.status_code == 429: 
            # rate limited; sleep for a while before retrying
            logging.warning('Received 429 rate-limit response.' )
            randomized_exponential_delay = (2 ** attempt) + random.random()
            time_to_sleep = min(randomized_exponential_delay, MAX_DELAY)
            time.sleep(time_to_sleep)

        else:
            # not rate limited, so no need to retry
            break


    if resp.status_code == 200:
        return resp.json()['response']['data']['items']

    else:
        logging.error('Error calling {0}. Status code: {1}. Response: {2}'.format(api_url,
                                                                                  resp.status_code,
                                                                                  resp.text))
        raise exception.ApiError('Get-Files call error. Check log for details.')



def get_files(project_id, authenticator):

    results = []

    offset = 0  # start at the first item
    limit = 100 # page size
    # loop to page through results
    while True: 
        items = get_files_one_page(offset, limit, project_id, authenticator)

        count = len(items)
        results.extend(items)

        if count < limit:
            # response contained fewer than we asked for, so we must be at the end
            break

        else:
            # continue loop to get another page
            offset += count 
            
    return results


def main():

    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
    
    project_id = 'x'#os.environ.get('DEV_PROJECT_ID')
    user_id = os.environ.get('DEV_USER_IDENTIFIER')
    user_secret = os.environ.get('DEV_USER_SECRET')

    if (project_id is None) or (user_id is None) or (user_secret is None):

        print('Missing environment variables. Did you run setenv?')
        sys.exit()

    authenticator = auth.Authenticator(user_id, user_secret)
    
    try:
        file_list = get_files(project_id, authenticator)

        for file in file_list:
            print(file['fileUri'])

        print('File count: {0}'.format(len(file_list)))            

    except exception.ApiError as error:

        logging.exception(error)
        print(error)
        

if __name__ == '__main__':
    main()


