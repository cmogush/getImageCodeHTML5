import os
from PIL import Image
from pathlib import Path

def getImageTag(repo, image, height, width, alt):
    return "&lt;img src=\""+repo+image+"\" height=\""+height+"\" width=\""+width+"\" alt=\""+alt+"\" /&gt;"

def getLocalTag(dir, image, height, width):
    return "<img src=\""+ dir + "\\" + image + "\" height=\"" + height + "\" width=\"" + width + "\" alt=\"\" align=\"right\"/>"

def writeImageCode(parent, currDir, file, repo, altTag):
    dir = parent+"\\"+currDir
    repo = repo+currDir+"/"
    file.write("<hr/><p>"+str(currDir)+"</p>")
    file.write("<table border-collapse: collapse; border: 1px solid transparent; cellpadding=\"5\" cellspacing=\"1\">\n")
    for f in os.listdir(dir):
        if os.path.isdir(dir+"\\"+f):
            writeImageCode(dir, f, file, repo, altTag)
        splitPath = (os.path.splitext(f))
        if not splitPath[1] == ".png" and not splitPath[1] == ".jpg":  # only get png and jpgs
            continue
        img = Image.open(dir + "/" + f)
        if altTag:
            img.show()
            print("Enter alt text for image"+f)
            alt = input("alt=")
        else:
            alt = ""
        width, height = img.size
        imgTag = getImageTag(repo, f, str(height), str(width), str(alt))
        localTag = getLocalTag(dir, f, str(height), str(width))
        file.write("<tr><td>"+localTag+"</td><td>"+str(imgTag)+"</td></tr>")
    file.write("</table>")

def main():
    print("Enter eSchoolware Repository (without quotes), e.g:")
    print("/suite/repository/workspace/courses/4275/12316/")
    repo = input("Input: ")
    # repo = r"/suite/repository/workspace/courses/4275/12316/"

    print("Enter local image directory to scan: ")
    cwd = Path(input("Input: "))
    # cwd = Path(r"D:\Edison\_NewDevelopment\2020\Math PSSA Prep\CE\images\assessment_pool_images")

    altTag = False
    if(input("Would you like manually alt-tag all of the images right now? (answer: y/n): ")=="y"):
        altTag = True

    parent = str(cwd.parent)
    dir = str(os.path.basename(cwd))
    imgCode = parent+"\\"+dir+"\html_image_code.html"

    """write the code to the file"""
    with open(imgCode, "w+") as file:
        file.write("<html>\n<body>\n")
        writeImageCode(parent, dir, file, repo, altTag)
        file.write("</body>\n</html>")

if __name__ == "__main__":
    main()