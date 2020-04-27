# getImageCodeHTML5
code to turn create html5 img tags for a repository

-will display the finished code in an html page, grouped by folder
-images will display on the left side, code on the right
-added ability to open each image as processed, to allow for manual alt-tagging
-will now output the file in the same dir as the program

How to use:

Input the relative repository directory. For example:
/suite/repository/workspace/courses/4275/12316/

Do NOT include quotation marks, and make sure there are forward-slashes at the beginning and end

Select the image directory for which you want to run the program. Make sure to include the FULL absolute path. Note, it will also run all ALL sub-folders within that directory. The program will not stop until all images have been gone through, so make sure not to do too many at once or it may become tedious/overwhelming.

The program will give you the option to also rename the files as well as add alt-text.

If renaming the files, each image will display and, then you simply enter the name of the file into the window and push return. No quotes are necessary

If adding alt-text, and you renamed the files, the alt-text will default to the renamed filename. Otherwise it will default to nothing. Simply enter return to keep the default alt-text. Otherwise, enter appropriate alt-text.

Once finished, the program will output an html file into the same local image directory, which will display the html code for the images in a table format.