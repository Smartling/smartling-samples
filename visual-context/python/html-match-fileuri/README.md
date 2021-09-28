## HTML context for any string in a specified file

This example initiates a matching process in which any string from the specified file URI that doesn't already have context and is in the uploaded HTML context file, is bound to matching strings in the uploaded context. To illustrate this, two separate test files are uploaded, each containing the same content: only strings from one of the files gets context.

To run the example, enter the following in a terminal window:

```
python3 html_match_file_uri.py
```

When you review the results in the CAT Tool (see [Checking the results](../README.md#checking-the-results)), you should see that only two of the four strings—the two from the file URI `html-match-fileuri-contentfile2.json` as specified in the script—have been bound to the uploaded context. The other two strings will have no visual context.

The approach used in this script suits situations where the content is split into separate files. For example, in the case of product content, if the information for each product is uploaded to Smartling in a separate file, then the corresponding context file could be uploaded and matched to the correct content file by URI.

For additional information, see [Context API examples](../README.md)
