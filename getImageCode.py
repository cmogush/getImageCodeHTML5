import os
from PIL import Image
from pathlib import Path


def writeHeader(file):
    """setup the header with the javascript function for copying text"""
    file.write("<html>\n<head>\n<script>\n")
    file.write("function copyTheText(id) {\n")
    file.write("/* Get the text field */\n")
    file.write("var copyText = document.getElementById(id);\n")
    file.write("/* Select the text field */\n")
    file.write("copyText.select();\n")
    file.write("/* Copy the text inside the text field */\n")
    file.write("document.execCommand(\"copy\");\n")
    file.write("/* Alert the copied text */\n")
    file.write("alert(\"Copied to clipboard: \" + copyText.value);}\n")
    file.write("</script>\n</head>\n<body>\n")

def getImageTag(repo, image, height, width, align, alt):
    # '&lt' used instead of '<' as it will be displaying the tag as text
    return "&lt;img src=\"" + repo + image + "\" height=\"" + height + "\" width=\"" + width + "\"" + align + " alt=\"" + alt + "\" /&gt;"


def getLocalTag(dir, image, height, width):
    return "<img src=\"" + dir + "\\" + image + "\" height=\"" + height + "\" width=\"" + width + "\" alt=\"\"/>"


def writeImageCode(parent, currDir, file, repo, altTag, rename, alignFractions):
    """function to write the image tags to the output html file"""
    # initial setup
    evenOdd = 0  # used for assigning every other row a different color
    align = ""  # set intial alignment
    dir = parent + "\\" + currDir  # get directory
    repo = repo + currDir + "/"  # set repo directory
    file.write("<hr/><p><h1>" + str(currDir) + "</h1></p>\n")
    file.write(
        "<table border-collapse: collapse; border: 1px solid transparent; cellpadding=\"5\" cellspacing=\"1\">\n")

    # iterate over the files in the directory
    for f in os.listdir(dir):
        if os.path.isdir(dir + "\\" + f):  # if f is a directory
            writeImageCode(dir, f, file, repo, altTag, rename)  # iterate over that directory (f)
        splitPath = (os.path.splitext(f))
        if not splitPath[1] == ".png" and not splitPath[1] == ".jpg":  # only get png and jpgs
            continue

        jsID = splitPath[0]  # set ID from filename, for javascript function

        # implement alt-tagging / renaming / alignment
        img = Image.open(dir + "/" + f)
        if altTag or rename or alignFractions:
            img.show()
            alt = splitPath[0]
            print("Current image name: " + splitPath[0])
        if rename:
            print("Enter new name for image below (or leave blank to keep current)")
            newName = input("New name: ")
            if not newName == "":
                os.rename(dir + "\\" + f, dir + "\\" + newName + splitPath[1])
                f = newName + splitPath[1]
                alt = newName
                jsID = newName

        if altTag:
            print("Suggested Alt-text: " + alt)
            print("Enter Alt-text below (or leave blank to keep suggestion)")
            newAlt = input("alt=")
            if not newAlt == "":
                alt = newAlt
        if alignFractions:
            if input("Is image a math equation and/or should be in-line with text? ('y' for yes, else leave blank): ") == 'y':
                align = " style=\"vertical-align: middle\""
            else:
                align = ""

        else:
            alt = ""

        # setup variables/attributes, final preparation before writing
        width, height = img.size
        imgTag = getImageTag(repo, f, str(height), str(width), str(align), str(alt))
        localTag = getLocalTag(dir, f, str(height), str(width))
        button = "<button onclick=\"copyTheText(my" + jsID + ".id)\">Copy</button>"

        if evenOdd == 0:
            bgcolor = "#dbe0ff"
            evenOdd = 1
        else:
            bgcolor = ""
            evenOdd = 0

        # write the image
        file.write("<tr bgcolor=\"" + bgcolor + "\">\n<td>" + localTag + "</td>\n")
        file.write("<!-- The button used to copy the text -->\n")
        file.write("<td>" + button + "</td>\n")
        file.write("<!-- The text field -->\n")
        file.write("<td><textarea rows=\"2\" style=\"width: 750\" type=\"text\" \nid=\"my" + jsID + "\">")
        file.write(str(imgTag) + "</textarea></td></tr>\n")
    file.write("</table>\n")

def main():
    #Copyright
    print('GetImageCode v1.04 - (c) 2020 Christopher Mogush ')
    print('-------------------------------------------------')
    # Get input from User
    print('Enter relative destination repository (without quotes)')
    print('e.g: /suite/repository/workspace/courses/4275/12316/')
    repo = input('Input: ')

    print("Enter local image directory to scan")
    imgDir = Path(input("Input: "))

    altTag = False
    rename = False
    alignFractions = False
    if "y" == input("Rename images? ('y' for yes, else leave blank): "): rename = True
    if "y" == input("Alt-tag images? ('y' for yes, else leave blank): "): altTag = True
    if "y" == input("Center math equations? ('y' for yes, else leave blank): "): alignFractions = True

    # Setup the variables from the user input
    parent = str(imgDir.parent)
    dir = str(os.path.basename(imgDir))
    imgCode = parent + "\\" + dir + "\html_image_code.html"

    # write the code to the file
    try:
        with open(imgCode, "w+") as file:
            writeHeader(file) # header
            writeImageCode(parent, dir, file, repo, altTag, rename, alignFractions) # body
            file.write("</body>\n</html>") # closing tags
    except:
        print("Not a valid directory")

if __name__ == "__main__":
    main()
