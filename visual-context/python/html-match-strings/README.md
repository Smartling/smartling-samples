### HTML context for any of a specified set of strings

This example uses a matching process in which any string from the specified groups of strings that doesn't already have context and is also in the uploaded HTML context file, is bound to matching string in the uploaded context. To illustrate this, a single content file is uploaded containing the same strings multiple times but with different keys: only some of the strings get context.

To run the example, enter the following in a terminal window:

```
python3 html_match_strings.py
```

When you review the results in the CAT Tool (see [Checking the results](../README.md#checking-the-results), you should see that only two of the four strings—the two whose keys start with 'topic.1' as specified in the script—have been bound to the uploaded context. The other two strings will have no visual context.

This approach may be suitable when all the content is in a single file, or small number of files. In this case, limiting the matching by URI is not specific enough and thus it has to be done by individual string. As this needs to be specified by hashcode, this script makes an additional API call to get the hashcodes of the uploaded strings, then it filters that list based on the keys of the strings (which are also returned in the same call).

#### Repeated strings in the context
You may have noticed that the string 'Lorem ipsum dolor sit amet', which appears in two places in the context file, has been highlighted in both places in the context view in the CAT Tool. This is the standard behavior of context, i.e., that all copies of a string within a context file are bound to that translatable string in the project. The method used in the [explicit binding](../html-explicit-binding) script allows you to override this behavior and choose precisely which context string to match.

For additional information, see [Context API examples](../README.md).
