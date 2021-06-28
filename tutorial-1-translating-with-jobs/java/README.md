# Tutorial 1 Java example
A Java program illustrating topics from   ['Tutorial 1 - Translation Jobs and Workflows'](https://help.smartling.com/hc/en-us/articles/1260804711510-Tutorial-1-Translation-Jobs-and-Workflows).

**ProcessJob.java**, uses the Smartling Java SDK to create a translation job in Smartling; then uploads some files to the job using job batches; checks progress of the translation job; and downloads the translated files when the job is complete.

## Prerequisites
To run the program, you need:

* Java installed
* Maven installed
* Smartling API token credentials for test project in Smartling

## Set Up
The code expects the following environment variables to be defined:

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

## Running the sample code
The Maven configuration file, `pom.xml`, is configured with a target for running the example:

```
mvn compile
mvn exec:java@run
```

Once the program starts checking the translation status, you will need to login to Smartling at [https://dashboard.smartling.com](https://dashboard.smartling.com), navigate to your test project, add translations, then submit them through the workflow. Once they are all in the Published workflow step, the program will download the completed translations. See the tutorial referenced above for details on this.