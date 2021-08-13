## HTML context for specific strings with explicit binding

This script specifies which strings from the project should be bound to which strings in the context file. It does this by pairing hashcodes with the values of `data-sl-anchor` attributes in the context HTML file. The test data is similar to the previous test, but in this case only one of the strings is highlighted in the context pane.

```
python3 bind-explicitly.py
```

When you review the results in the CAT Tool (see [Checking the results](../README.md#checking-the-results)), you should see that the strings whose keys start with 'topic.1' or 'meta.1' as specified in the script—have been bound to the uploaded context. The other strings will have no visual context. In addition, and in contrast with the previous examples, only one instance of the string 'Topic name' is highlighted in the context pane of the CAT Tool.

The explicit-binding approach allows precise control over which strings in the context file are bound to which strings in the project. It may be suitable when the same string appears in multiple places in the context file, and the correct one must be chosen. However, it requires the addition of the `data-sl-anchor` attributes to the context file. This may be simple to do if the context integration process is responsible for generating the context HTML files. On the other hand, if the context files are being extracted from a different system, such as a website, it might be more difficult to achieve. The `data-sl-anchor` attribute used in the binding process is also used for sorting strings in the translation interface allowing translators to work on them in the order that they appear in the context. Therefore it's important to set this attribute to an integer value, and to maintain a mapping between this value and the corresponding string key.

For additional information, see [Context API examples](../README.md)

