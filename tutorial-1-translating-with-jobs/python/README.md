# Tutorial 1 Python scripts
Python scripts illustrating topics from   ['Tutorial 1 - Translation Jobs and Workflows](https://help.smartling.com/hc/en-us/articles/1260804711510-Tutorial-1-Translation-Jobs-and-Workflows).

The following scripts are included:

* **start-translation-job.py**. Create a translation job in Smartling and upload some files to it for translation.
* **status-translation-job.py**. Check on the progress of a translation job.
* **download-translation-job.py**. Download the translated files from a translation job.

## Prerequisites
To run the sample scripts, you need:

* Python installed
* Python 'requests' package installed
* Smartling API token credentials for test project in Smartling

## Set Up
The scripts expect the following environment variables to be defined:

* **DEV_PROJECT_ID**. The UID of the Smartling test project.
* **DEV_USER_IDENTIFIER**. The user identifier from your API token.
* **DEV_USER_SECRET**. The user secret from your API token.

To set these up, download a copy of the either setenv.sh (for Mac and Linux) or setenv.cmd (for Windows) from the root directory of the repository, update them with your own information, then run them in the terminal where you'll be running the scripts:

Mac or Linux
```
source ./setenv.sh
```
Windows
```
.\setenv.cmd
```

## Running the scripts
The examples below assume that the command `python3` will run the Python interpreter. You may need to adjust this for your platform, for example, using `py` on Windows.
### start-translation-job.py
Create a translation job in Smartling and upload some files to it for translation. You supply the job name as a parameter. The files to upload and the locales to translate them into are hard-coded in the script and can be modified there. To create a job named 'Test Job 1', enter:
```
python3 start-translation-job.py 'Test Job 1'
```
The job UID is printed to the screen. You can use this ID to check the status of the job using the `status-translation-job.py` script. Errors are also printed to the screen and should indicate what the cause is. For example, if you run the above command twice, you should see an error saying that the job already exists.

To see the job in Smartling, log in to Smartling at [https://dashboard.smartling.com](https://dashboard.smartling.com), navigate to your test project, then click on the Jobs tab between the Summary and Files tabs.

Note that the script adds the job UID to the URIs of the uploaded files. This is to simplify testing by allowing each job you create to have its own copy of the test files. This would not typically be done in a production integration. For more information, see the Namespace section here: [Strings](https://help.smartling.com/hc/en-us/articles/360049585953-Strings)

### status-translation-job.py
Checks on the progress of a translation job by job ID.
```
python3 status-translation-job.py oeavfjdjhrqo
```
You can get the job ID from the output of the `start-translation-job` script as decribed above. You can also get the job ID from within the Smartling dashboard by clicking into the job: the job UID is at the end of the URL after the ':' character. And you can get the job ID by calling the [List jobs](https://api-reference.smartling.com/#operation/getJobsByProject) API endpoint passing the job name as a parameter.

The script prints the 'percentage complete' value for the job to the screen. For the job to make progress, it needs to be 'authorized' (either via the dashboard, or by modifying the `start-translation-job.py` script), and its content translated and advanced through the workflow. See the [tutorial](https://help.smartling.com/hc/en-us/articles/1260804711510-Tutorial-1-Translation-Jobs-and-Workflows) for details.

### download-translation-job.py
Downloads the translated files from the translation job specified by the job ID parameter.
```
python3 status-translation-job.py oeavfjdjhrqo
```
See status-translation-job.py above for where to find the job ID.

The URIs of the files and the target locales (languages) are hardcoded in the script to match those used in the `start-translation-job.py` script. The downloaded translated files have the locale IDs appended to their names.

Note that the files will show the source language unless they are actually translated in the Smartling platform, either manually or through an automated method such as machine translation or SmartMatch.
