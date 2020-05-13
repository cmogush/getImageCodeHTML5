import os
from PIL import Image
from pathlib import Path


def getImageTag(repo, image, height, width, align, alt):
    # '&lt' used instead of '<' as it will be displaying the tag as text
    return "&lt;img src=\"" + repo + image + "\" height=\"" + height + "\" width=\"" + width + "\" align=\"" + align + "\" alt=\"" + alt + "\" /&gt;"


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
            if (input("Type 'y' if image is a fraction (and should be aligned center), else leave blank: ") == 'y'):
                align = "style=\"vertical-align: middle\""
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
            bgcolor = "#d1feff"
            evenOdd = 1
        else:
            bgcolor = "white"
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
    print("Enter eSchoolware Repository (without quotes), e.g:")
    print("/suite/repository/workspace/courses/4275/12316/")
    repo = input("Input: ")
    # repo = r"/suite/repository/workspace/courses/4275/12316/"

    print("Enter local image directory to scan: ")
    imgDir = Path(input("Input: "))
    # imgDir = Path(r"D:\Edison\_NewDevelopment\2020\Math PSSA Prep\CE\images\assessment_pool_images")

    currDir = os.getcwd()

    altTag = False
    rename = False
    alignFractions = False
    if (input("Would you like manually rename all of the images right now? (answer: y/n): ") == "y"):
        rename = True
    if (input("Would you like manually alt-tag all of the images right now? (answer: y/n): ") == "y"):
        altTag = True
    if (input("Would you like center all fractions (to be in-line with text) right now? (answer: y/n): ") == "y"):
        alignFractions = True

    parent = str(imgDir.parent)
    dir = str(os.path.basename(imgDir))
    imgCode = parent + "\\" + dir + "\html_image_code.html"
    print(imgCode)

    """write the code to the file"""
    with open(imgCode, "w+") as file:
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

        """write the body"""
        writeImageCode(parent, dir, file, repo, altTag, rename, alignFractions)

        """close the html page"""
        file.write("</body>\n</html>")


if __name__ == "__main__":
    main()
