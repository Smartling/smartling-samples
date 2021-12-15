# Tutorial 1 Python SDK example
A Python program illustrating topics from   ['Tutorial 1 - Translation Jobs and Workflows'](https://help.smartling.com/hc/en-us/articles/1260804711510-Tutorial-1-Translation-Jobs-and-Workflows).

**process-job.py**, uses the Smartling Python SDK to create a translation job in Smartling; then uploads some files to the job using job batches; checks progress of the translation job; and downloads the translated files when the job is complete.

## Prerequisites
To run the program, you need:

* Python installed
* Smartling API token credentials for test project in Smartling

## Set Up
The code expects the following environment variables to be defined:

* **SL_PROJECT_ID**. The UID of the Smartling test project.
* **SL_USER_IDENTIFIER**. The user identifier from your API token.
* **SL_USER_SECRET**. The user secret from your API token.
* **SL_LOCALE**. Any locale code, such as 'fr-FR'. 


## Running the sample code
Once the above is done, the script can be run as follows:

```
python3 process-job.py
```

When the program starts checking the translation status, you will need to login to Smartling at [https://dashboard.smartling.com](https://dashboard.smartling.com), navigate to your test project, and to the job create by the script, add translations, then submit them through the workflow. Once they are all in the Published workflow step, the program will download the completed translations. See the tutorial referenced above for details on this.
