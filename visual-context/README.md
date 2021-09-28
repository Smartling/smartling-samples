# Visual Context examples

Visual Context gives translators the visual information they need to produce high-quality translations first time. The presence of visual context is the difference between the two images below of the translation interface.

### Translating with Visual Context:
![Visual Context](https://raw.githubusercontent.com/Smartling/smartling-samples/master/visual-context/images/context.png)

### Translating *without* Visual Context:
![No Visual Context](https://raw.githubusercontent.com/Smartling/smartling-samples/master/visual-context/images/nocontext.png)

When translating website copy, visual context can display--directly in the translation interface--the actual web page where the content will appear; when translating product copy, visual context can show product imagery; and when translating video subtitles, visual context can display the correct section of the video. 

Smartling provides a number of tools for capturing and uploading visual context to the platform (see [Capturing Visual Context](https://help.smartling.com/hc/en-us/sections/360001682353-Capturing-Visual-Context)). In addition, context can be uploaded manually to the dashboard, or can be automatically uploaded via API. The API approach to uploading context provides the greatest control over the process. 

## Context integration steps

The high-level steps for integrating context is:

1. **Upload the content.** The content to be translated should be uploaded to Smartling before the context is uploaded.
2. **Generate the context.** For example, this might involve capturing the HTML for a rendered web page or web app, or generating screenshots from a mobile app.
3. **Upload the context.** Once the context file (HTML, image or video) is generated, it's uploaded to the Smartling platform. For video, it's also possible to upload a URL.
4. **Associate the context with the content being translated.** A number of approaches to this are illustrated in the examples.

It's also possible to combine steps 3 and 4 in a single API call.

## Context types

The following context types can be uploaded explicitly to Smartling via API:

- **HTML.** Uploaded as an HTML file which can reference publicly accessible resources such as images, or can include these resources inline in the HTML file.
- **Image.** These can be uploaded as image files, or as a video (or URL), from which images are extracted.
- **Video.** Video context is supported for subtitle content, such as SRT files.

Smartling also supports 'implicit' context which is extracted from the content file itself, for example when an HTML file or Word document is uploaded for translations. These examples cover explicit context upload.

## Code examples

This folder illustrates use of the API to upload different context types and to control how the context is matched up with the content being translated.

See subfolders below for the code examples:

* [Python](python)


