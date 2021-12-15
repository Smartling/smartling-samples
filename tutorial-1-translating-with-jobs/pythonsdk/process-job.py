import sys
import time


from smartlingApiSdk.Credentials import Credentials
from smartlingApiSdk.api.JobsApi import JobsApi
from smartlingApiSdk.api.JobBatchesV2Api import JobBatchesV2Api
from smartlingApiSdk.api.FilesApi import FilesApi

FILE_LIST = [
    'test-files/test1.json',
    'test-files/test2.json'
]
FILE_TYPE = 'json'
LOCALE_LIST = ['fr-FR']
AUTHORIZE = True 

def main():

    # Credentials expects the following environment variables to be defined:
    # SL_USER_IDENTIFIER, SL_USER_SECRET, SL_PROJECT_ID
    creds = Credentials()

    # instantiate API clients
    jobs_api = JobsApi(creds.MY_USER_IDENTIFIER, creds.MY_USER_SECRET, creds.MY_PROJECT_ID)
    job_batches_api = JobBatchesV2Api(creds.MY_USER_IDENTIFIER, creds.MY_USER_SECRET, creds.MY_PROJECT_ID)
    files_api = FilesApi(creds.MY_USER_IDENTIFIER, creds.MY_USER_SECRET, creds.MY_PROJECT_ID)
    
    # create job
    print('Creating job...')
    job_name = 'Test Job ' + str(int(time.time()))
    resp, status = jobs_api.addJob(job_name)
    if status != 200:
        print(status, resp)
        sys.exit()
    job_uid = resp.data.translationJobUid
    print('Job created.')


    # create job batch
    print('Create job batch...')
    # include job_uid in file URI to avoid confusion during testing
    uri_list = [job_uid + '/' + file_name for file_name in FILE_LIST]
    resp, status = job_batches_api.createJobBatchV2(authorize=AUTHORIZE, 
                                                    translationJobUid=job_uid, 
                                                    fileUris=uri_list)
    if status != 200:
        print(status, resp)
        sys.exit()
    batch_uid = resp.data.batchUid
    print('Job batch created.')


    # upload files to job batch    
    print('Adding files to batch...')
    for file_name in FILE_LIST:
        uri = job_uid + '/' + file_name
        resp, status = job_batches_api.uploadFileToJobBatchV2(batchUid=batch_uid, 
                                                              file=file_name, 
                                                              fileUri=uri, 
                                                              fileType=FILE_TYPE, 
                                                              authorize=AUTHORIZE, 
                                                              localeIdsToAuthorize=LOCALE_LIST)
        if status != 202:
            print(status, resp)
            sys.exit()
        print('Added file ' + file_name)


    # check job status until complete
    print('Will check job status every 10 seconds until complete. Log in to dashboard to complete translations.')
    while True:
        resp, status = jobs_api.getJobProgress(translationJobUid=job_uid)
        if status != 200:
            print(status, resp)
            sys.exit()
        progress = resp.data.progress
        if progress is not None:
            percent_complete = progress['percentComplete']
        else:
            percent_complete = 0
        print('Job progress: ' + str(percent_complete) + '% complete')
        if percent_complete == 100:
            break
        else:
            time.sleep(10)
    
    
    # download translated files
    for file_name in FILE_LIST:
        for locale in LOCALE_LIST:
            uri = job_uid + '/' + file_name
            resp, status = files_api.downloadTranslatedFileSingleLocale(localeId=locale, fileUri=uri)
            if status != 200:
                print(status, resp)
                sys.exit()
            # insert locale_id before '.json' extension in translated file name
            translated_file_name = file_name[:-5] + '_' + locale + file_name[-5:]
            with open(translated_file_name, 'wb') as f:
                f.write(resp)
                print('Downloaded ' + translated_file_name)


if __name__ == '__main__':
    main()



