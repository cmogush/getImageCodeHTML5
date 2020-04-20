import os
from PIL import Image
from pathlib import Path

def getImageTag(repo, image, height, width):
    return "<img src=\""+repo+image+"\" height=\""+height+"\" width=\""+width+"\" alt=\"\" />"

def writeImageCode(parent, currDir, file, repo):
    dir = parent+"\\"+currDir
    repo = repo+currDir+"/"
    for f in os.listdir(dir):
        if os.path.isdir(dir+"\\"+f):
            writeImageCode(dir, f, file, repo)
        splitPath = (os.path.splitext(f))
        if not splitPath[1] == ".png" and not splitPath[1] == ".jpg":  # only get png and jpgs
            continue
        img = Image.open(dir + "/" + f)
        width, height = img.size
        file.write(getImageTag(repo, f, str(height), str(width)) + "\n")

def main():
    print("Enter eSchoolware Repository (without quotes), e.g:")
    print("/suite/repository/workspace/courses/4275/12316/")
    repo = input("Input: ")
    # repo = r"/suite/repository/workspace/courses/4275/12316/"

    print("Enter local image directory to scan: ")
    # cwd = Path(r"D:\Edison\_NewDevelopment\2020\Math PSSA Prep\CE\images\assessment_pool_images")
    cwd = Path(input("Input: "))

    parent = str(cwd.parent)
    dir = str(os.path.basename(cwd))
    imgCode = parent+"\\"+dir+"\html_image_code.txt"

    """write the code to the file"""
    with open(imgCode, "w+") as file:
        writeImageCode(parent, dir, file, repo)

if __name__ == "__main__":
    main()