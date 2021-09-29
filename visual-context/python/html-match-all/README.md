## HTML context for any project string

This example uses a matching process in which any string in the project that doesn't already have context and is found in the uploaded HTML context file, is bound to matching strings in uploaded context. To illustrate this, two separate test files are uploaded first, each containing the same content: the context gets bound to the strings in both files.

To run the example, enter the following in a terminal window:

```
python3 html_match_all.py
```

When you review the results in the CAT Tool (see [Checking the results](../README.md#checking-the-results)), you should see that all four strings—two from each file—have been bound to the uploaded context.

This is the simplest context-matching approach, but it runs the risk of matching context to the wrong string if the same string can appear multiple times in a project with different contexts. If that happens only rarely, then this approach may be sufficient.

For additional information, see [Context API examples](../README.md)
