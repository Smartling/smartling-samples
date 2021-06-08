# Getting Started Java SDK Examples
Java applications illustrating topics from the [Getting Started](https://help.smartling.com/hc/en-us/articles/1260804661570-Getting-Started) tutorial.

The following examples are included:

* **Upload.java**. Upload a file to Smartling
* **DownloadPseudo.java**. Download a pseudotranslated file from Smartling.

## Prerequisites
To run the sample code, you need:

* Java installed
* Maven installed
* Smartling API token credentials for a test project in Smartling

## Set Up
The code expects the following environment variables to be defined:

* **DEV_PROJECT_ID**. The UID of the Smartling test project.
* **DEV_USER_IDENTIFIER**. The user identifier from your API token.
* **DEV_USER_SECRET**. The user secret from your API token.

To set these up, download a copy of the either `setenv.sh` (for Mac and Linux) or `setenv.cmd` (for Windows) from the root directory of the repository, update them with your own information, then run them in the terminal where you'll be running the examples:

Mac or Linux
```
source ./setenv.sh
```
Windows
```
.\setenv.cmd
```

## Running the sample code
The Maven configuration file, `pom.xml`, is configured with targets for running the examples.
### Upload
Uploads a file to Smartling, taking the file name and type as parameters, and uses the file name as the URI in Smartling. The pom.xml file includes the command-line arguments, which can be modified as needed. To compile and run the sample, enter the following commands in at terminal at the location where the pom.xml file is.
```
mvn compile
mvn exec:java@upload
```
If modifying the example to use different file types, the list of valid file-type values can be found under the fileType parameter for the [Upload file documentation](https://api-reference.smartling.com/#operation/uploadSourceFile). Details on supported file types can be found at [Supported File Types](https://help.smartling.com/hc/en-us/articles/360007998893-Supported-File-Types)

To see your uploaded file in Smartling, log in to Smartling at [https://dashboard.smartling.com](https://dashboard.smartling.com), navigate to your test project, then click on the Files tab.

### DownloadPseudo
Downloads a pseudotranslated file from Smartling, taking the file URI (which will be the file name if the Upload sample was used to upload) as the first argument, the name to be used for the downloaded file as the second argument, and any valid locale code from the project as the third argument. The command-line arguments are configured in the pom.xml file and can be modified as needed there. To compile and run the sample, enter the following commands in at terminal at the location where the pom.xml file is.
```
mvn compile
mvn exec:java@download
```
