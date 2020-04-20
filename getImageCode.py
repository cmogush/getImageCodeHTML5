import os
from PIL import Image
from pathlib import Path

def getImageTag(repo, image, height, width, alt):
    return "&lt;img src=\""+repo+image+"\" height=\""+height+"\" width=\""+width+"\" alt=\""+alt+"\" /&gt;"

def getLocalTag(dir, image, height, width):
    return "<img src=\""+ dir + "\\" + image + "\" height=\"" + height + "\" width=\"" + width + "\" alt=\"\"/>"

def writeImageCode(parent, currDir, file, repo, altTag, rename):
    evenOdd = 0
    dir = parent+"\\"+currDir
    repo = repo+currDir+"/"
    file.write("<hr/><p><h1>"+str(currDir)+"</h1></p>")
    file.write("<table border-collapse: collapse; border: 1px solid transparent; cellpadding=\"5\" cellspacing=\"1\">\n")
    for f in os.listdir(dir):
        if os.path.isdir(dir+"\\"+f):
            writeImageCode(dir, f, file, repo, altTag, rename)
        splitPath = (os.path.splitext(f))
        if not splitPath[1] == ".png" and not splitPath[1] == ".jpg":  # only get png and jpgs
            continue

        img = Image.open(dir + "/" + f)
        if altTag or rename:
            img.show()
            alt = splitPath[0]
            print("Current image name: "+splitPath[0])
        if rename:
            print("Enter new name for image below (or leave blank to keep current)")
            newName = input("New name: ")
            if not newName == "":
                os.rename(dir+"\\"+f,dir+"\\"+newName+splitPath[1])
                f = newName + splitPath[1]
                alt = newName
        if altTag:
            print("Suggested Alt-text: "+alt)
            print("Enter Alt-text below (or leave blank to keep suggestion)")
            newAlt = input("alt=")
            if not newAlt == "":
                alt = newAlt

        else:
            alt = ""
        width, height = img.size
        imgTag = getImageTag(repo, f, str(height), str(width), str(alt))
        localTag = getLocalTag(dir, f, str(height), str(width))

        if evenOdd == 0:
            bgcolor = "#d1feff"
            evenOdd = 1
        else:
            bgcolor = "white"
            evenOdd = 0

        file.write("<tr bgcolor=\""+bgcolor+"\"><td>"+localTag+"</td><td>"+str(imgTag)+"</td></tr>")
    file.write("</table>")

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
    if (input("Would you like manually rename all of the images right now? (answer: y/n): ") == "y"):
        rename = True
    if(input("Would you like manually alt-tag all of the images right now? (answer: y/n): ")=="y"):
        altTag = True

    parent = str(imgDir.parent)
    dir = str(os.path.basename(imgDir))
    imgCode = parent+"\\"+dir+"\html_image_code.html"
    print(imgCode)

    """write the code to the file"""
    with open(imgCode, "w+") as file:
        file.write("<html>\n<body>\n")
        writeImageCode(parent, dir, file, repo, altTag, rename)
        file.write("</body>\n</html>")

if __name__ == "__main__":
    main()