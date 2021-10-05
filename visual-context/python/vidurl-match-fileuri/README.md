## Video context for strings in a specified subtitle file (SRT or VTT)

This example associates strings in a video subtitle file with the corresponding sections of video referenced by URL. This allows the translator to see the video in the translation interface, and to have it automatically move to the correct part of the video depending on which subtitle the translator is working on.

To run the example, enter the following in a terminal window:

```
python3 vidurl_match_subtitles.py
```

When you review the results in the CAT Tool (see [Checking the results](../README.md#checking-the-results)), you should see that each string has been matched with the appropriate section of the video. 

In order for the video to be processed in this way (as opposed to having images extracted from it for image context), it's necessary to specify a subtitle file URI in the `contentFileUri` parameter of the context matching call.

For additional information, see [Context API examples](../README.md)
