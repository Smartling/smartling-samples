## Image context for any string in a specified file

This example initiates a matching process in which any string from the specified file URI that doesn't already have context and is found via OCR in the uploaded context image file, is bound to matching region of the context image. To illustrate this, a test files containing two strings is uploaded, only one of which is contained in the context file: only the string found in the context file gets context.

To run the example, enter the following in a terminal window:

```
python3 image_match_file_uri.py
```

When you review the results in the CAT Tool (see [Checking the results](../README.md#checking-the-results)), you should see that only one of the two strings from the file URI `image-match-fileuri-contentfile1.json` has been bound to the uploaded context. The other string will have no visual context.

Restricting context matching by URI suits situations where the content is split into separate files. For example, in the case of product content, if the information for each product is uploaded to Smartling in a separate file, then the corresponding context file could be uploaded and matched to the correct content file based on the URI.

For additional information, see [Context API examples](../README.md)
