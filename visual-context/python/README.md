# Context API Python examples

Sample scripts illustrating the various ways to associate visual context with strings in Smartling using the [Context API](https://api-reference.smartling.com/#tag/Context).

Each script is in a separate subdirectory which also contains the associated context file and data files. The script first uploads the test files and adds them to a job, then uploads the context and performs the matching process.

If you need to run the scripts multiple times, for example due to changes or problems, it might be necessary to cancel and delete the jobs and/or context from Smartling between runs. This can be done in the Smartling dashboard. For example, running the same script twice will fail because the job to be created already exists; to resolve, cancel and delete the job in the dashboard.

## Prerequisites
* Python installed. The examples below assume that Python is installed and `python3` is the command to run it. You may need to adjust this for your platform.
* Python *requests* package installed.
* Test project in Smartling with fr-FR as one of the target locales (script can be modified to use a different locale)
* API token credentials for the test project available.

## Set Up
The scripts expect the following environment variables to be defined:

* **DEV_PROJECT_ID**. The UID of the Smartling test project you're using.
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

## Checking the results

After each of the scripts below is run, a new job is created in Smartling and authorized for translation. To see how context has been attached:

1. Log in to Smartling at [https://dashboard.smartling.com](https://dashboard.smartling.com) and navigate to your test project
2. Click on the project *Jobs* tab (next to the *Summary* tab)
3. Click on the newly created job (should be listed first)
4. Click the three dots under *Actions* on the right, and select *Edit in CAT Tool*. (You might need to wait a few seconds until the job is authorized and 'in progress' before doing this.)
5. Move the cursor between the translatable strings to see the context for each string. You can check the *Additional Details* section in the upper right to see the file URI and other information.

## HTML context

**Note:** The HTML context files used in these examples reference publicly hosted resources such as images and CSS. If it's not possible to make the context resources publicly accessible, then they can also be inlined (e.g., using  `src="data:image/jpeg;base64,imagedata...`) directly in the HTML file being uploaded. Alternatively, the IP address of Smartling's context loading service can be whitelisted restricting access to the images to requests from that server.

* [HTML context for any project string](html-match-all)
* [HTML context for any string in a specified file](html-match-fileuri)
* [HTML context for any of a specified set of strings](html-match-strings)
* [HTML context for specific strings with explicit binding](html-explicit-binding)

