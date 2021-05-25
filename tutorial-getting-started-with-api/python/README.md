# Getting Started Python scripts
Python scripts illustrating topics from the ['Getting Started' tutorial](https://help.smartling.com/hc/en-us/articles/1260804661570-Getting-Started).

The following scripts are included:

* **slupload.py**. Upload a file to Smartling
* **sldownloadpseudo.py**. Download a pseudotranslated file from Smartling.

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

To set these up, download a copy of the either setenv.sh (for Mac and Linux) or setenv.cmd (for Windows) from the root directory of the repo, update them with your own information, then run them in the terminal where you'll be running the scripts:

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
### slupload.py
Uploads a file to Smartling, taking the file name and type as parameters, and uses the file name as the URI in Smartling. For example, to upload the sample JSON file, you would enter:
```
python3 slupload.py strings.json json
```
This list of valid file-type values can be found under the fileType parameter for the [Upload file documentation](https://api-reference.smartling.com/#operation/uploadSourceFile). Details on supported file types can be found at [Supported File Types](https://help.smartling.com/hc/en-us/articles/360007998893-Supported-File-Types)

To see your uploaded file in Smartling, log in to Smartling at [https://dashboard.smartling.com](https://dashboard.smartling.com), navigate to your test project, then click on the Files tab.

### sldownloadpseudo.py
Downloads a pseudotranslated file from Smartling. Takes the file URI (which will be the file name if the slupload.py script was used to upload) as the first paramter. The second parameter can be any locale code that is defined in the Smartling project:
```
python3 sldownloadpseudo.py strings.json fr-FR
```
The downloaded file will have '_pseudo' added to the name.
