# Visual Context examples

Visual Context gives translators the visual information they need to produce high-quality translations first time. For example, when translating website copy, visual context can display--directly in the translation interface--the actual web page where the content will appear; when translating product copy, visual context can show product imagery; and when translating video subtitles, visual context can display the correct section of the video. Smartling provides a number of tools for capturing and uploading visual context to the platform (see [Capturing Visual Context](https://help.smartling.com/hc/en-us/sections/360001682353-Capturing-Visual-Context)). In addition, context can be uploaded manually to the dashboard, or can be automatically uploaded via API. The API approach to uploading context provides the greatest control over the process. 

This folder illustrates use of the API to upload different context types and to control how the context is matched up with the content being translated.

The high-level flow for integrating context is:

1. **Upload the content.** The content to be translated should be uploaded to Smartling before the context is uploaded.
2. **Generate the context.** This might involve capturing the HTML for a rendered web page or web app, or generating screenshots from a mobile app.
3. **Upload the context.** Once the context file (HTML, image or video) is generated, it's uploaded to the Smartling platform.
4. **Associate the context with the content being translated.** There are a number of approaches to this, which are illustrated in the examples.

It's also possible to combine steps 3 and 4 in a single API call.

See subfolders below for the scripts:

* [Python scripts](python)


