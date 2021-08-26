# Tutorial 1 NodeJS example
A NodeJS script illustrating topics from   ['Tutorial 1 - Translation Jobs and Workflows'](https://help.smartling.com/hc/en-us/articles/1260804711510-Tutorial-1-Translation-Jobs-and-Workflows).

**index.ts**, uses the Smartling NodeJS SDK to create a translation job in Smartling; then uploads some files to the job using job batches; checks progress of the translation job; and downloads the translated files when the job is complete.

## Prerequisites
To run the program, you need:

* NodeJS installed
* Smartling API token credentials for test project in Smartling

## Running the sample code
The code expects the following environment variables to be defined:

* **DEV_PROJECT_ID**. The UID of the Smartling test project.
* **DEV_USER_IDENTIFIER**. The user identifier from your API token.
* **DEV_USER_SECRET**. The user secret from your API token.

```
npm install
npm run build
DEV_PROJECT_ID=<DEV_PROJECT_ID> DEV_USER_IDENTIFIER=<DEV_USER_IDENTIFIER> DEV_USER_SECRET=<DEV_USER_SECRET> node built/index.js
```

Once the program starts checking the translation status, you will need to login to Smartling at [https://dashboard.smartling.com](https://dashboard.smartling.com), navigate to your test project, add translations, then submit them through the workflow. Once they are all in the Published workflow step, the program will download the completed translations. See the tutorial referenced above for details on this.
