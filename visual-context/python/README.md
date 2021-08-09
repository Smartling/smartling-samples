# Context API examples

Sample scripts illustrating the various ways to associate visual context with strings in Smartling using the context API:

### HTML context examples

* **html-match-all**. Associates uploaded HTML context with any matching project string.
* **html-match-fileuri**. Associates uploaded HTML context with any matching strings from a previously uploaded file based on the file URI.
* **html-match-strings**. Associates uploaded HTML context with any matching strings from within a set of previously uploaded strings based on string hashcode.
* **html-explicit-binding.py**. Associates individual strings in an uploaded HTML context with previously uploaded content strings based on a binding between the string hashcode and an element ID in the context file.

The scripts are listed in order of increasing control of the matching process. Which script is appropriate for a given situation depends on a number of factors touched on below.

## Test files
Test files containing translatable content in JSON format and an HTML context file for each script are provided in the same subdirectory as the associated script. The script first uploads the test files and adds them to a job, then uploads the context and performs the matching process.

### Context HTML format

The HTML context files used in these examples are simple and have images embedded inline using  `src="data:image/jpeg;base64,imagedata...` which makes them self-contained. It's also possible to use external links for images and other resources: as long as they're accessible over the internet, Smartling will load them in as part of the context processing process. And of course, more elaborate HTML context, reflecting a final rendered web page, can be used too.

## Prerequisites
* Python installed. The examples below assume that Python is installed and `python3` is the command to run it. You may need to adjust this for your platform.
* Python *requests* package installed.
* Test project in Smartling with fr-FR as one of the target locales (script can be modified to use a different locale)
* API token credentials for the test project available.

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

## Checking the results

After each of the script pairs below is run, a new job is created in Smartling and authorized for translation. To see how context has been attached:

1. Log in to Smartling at [https://dashboard.smartling.com](https://dashboard.smartling.com) and navigate to your test project
2. Click on the project *Jobs* tab (next to the *Summary* tab)
3. Click on the first job listed
4. Click the three dots under *Actions* on the right, and select *Edit in CAT Tool*. (You might need to wait a few seconds until the job is authorized and 'in progress' before doing this.)
5. Move the cursor between the translatable strings to see the context for each string. You can check the *Additional Details* section in the upper right to see the file URI and other information.

## Running the scripts

If you need to run the scripts multiple times, for example due to changes or problems, it might be necessary to cancel and delete the jobs and/or context from Smartling between runs. This can be done in the Smartling dashboard. The upload of test files will fail if a job already exists with the same name.

### html\_match\_all.py

This script initiates a matching process in which any string in the project that doesn't already have context, and is found in the uploaded HTML context file, is bound to this uploaded context. To illustrate this, two separate test files are uploaded first, each containing the same content; the context gets bound to the strings in both files.

```
python3 html_match_all.py
```

When you review the results in the CAT Tool (see *Checking the results* above), you should see that all four strings—two from each file—have been bound to the uploaded context.

This is the simplest matching approach, but it runs the risk of matching context to the wrong string in the project if the same string can appear multiple times in a project with different contexts. If that happens only rarely, then this approach may be sufficient.

### html\_match\_fileuri.py

This script initiates a matching process in which any string from the specified file URI that doesn't already have context and is in the uploaded HTML context file, is bound to the uploaded context. To illustrate this, two separate test files are uploaded, each containing the same content; only strings from one of the files gets context.


```
python3 html_match_file_uri.py
```

When you review the results in the CAT Tool (see *Checking the results* above), you should see that only two of the four strings—the two from the file URI `html-match-fileuri-contentfile2.json` as specified in the script—have been bound to the uploaded context. The other two strings will have no visual context.

The approach used in this script suits situations where the content is split into separate files. For example, in the case of product content, if the information for each product is uploaded to Smartling in a separate file, then the corresponding context file could be uploaded and matched to the correct content file by URI.

### html\_match\_strings.py

This script initiates a matching process in which any string from the specified groups of strings that doesn't already have context and is also  in the uploaded HTML context file, is bound to the uploaded context. To illustrate this, a single content file is uploaded containing the same strings multiple times but with different keys; only some of the strings get context.

```
python3 match-strings.py
```

When you review the results in the CAT Tool (see *Checking the results* above), you should see that only two of the four strings—the two whose keys start with 'topic.1' as specified in the script—have been bound to the uploaded context. The other two strings will have no visual context.

This approach may be suitable when all the content is in a single file, or small number of files, such that limiting the matching by URI is not specific enough and thus it has to be done by individual string. As this needs to be specified by hashcode, this script makes an additional API call to get the hashcodes of the uploaded strings, then it filters that list based on the keys of the strings (which are also returned in the same call).

#### Repeated strings in the context
You may have noticed that the string 'Topic name', which appears in two places in the context file, has been highlighted in both places in the context view in the CAT Tool. This is the standard behavior of context, i.e., that all copies of a string within a context file are bound to that translatable string in the project. The method used in the next script allows you to override this behavior and choose precisely which string to match.


### html\_explicit\_binding.py

This script specifies which strings from the project should be bound to which strings in the context file. It does this by pairing hashcodes with the values of `data-sl-anchor` attributes in the context HTML file. The test data is similar to the previous test, but in this case only one of the strings is highlighted in the context pane.

```
python3 bind-explicitly.py
```

When you review the results in the CAT Tool (see *Checking the results* above), you should see that the strings whose keys start with 'topic.1' or 'meta.1' as specified in the script—have been bound to the uploaded context. The other strings will have no visual context. In addition, and in contrast with the previous examples, only one instance of the string 'Topic name' is highlighted in the context pane of the CAT Tool.

The explicit-binding approach allows precise control over which strings in the context file are bound to which strings in the project. It may be suitable when the same string appears in multiple places in the context file, and the correct one must be chosen. However, it requires the addition of the `data-sl-anchor` attributes to the context file. This may be simple to do if the context integration process is responsible for generating the context HTML files. On the other hand, if the context files are being extracted from a different system, such as a website, it might be more difficult to achieve. The `data-sl-anchor` attribute used in the binding process is also used for sorting strings in the translation interface allowing translators to work on them in the order that they appear in the context. Therefore it's important to set this attribute to an integer value, and to maintain a mapping between this value and the corresponding string key.
