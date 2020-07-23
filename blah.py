import os
import re

base = "asdf"
imageBase = base + "/kimi_wa_midara_na_boku_no_joou" + "-{:03d}-{:03d}.jpg"

def fixDir(filename):
    dirPath = os.path.join(base, filename)
    m = re.findall(r"\d+$", filename)
    cNumber = int(m[0])
    print cNumber
    allfiles = os.listdir(dirPath)
    if len(allfiles) == 0:
        os.rmdir(dirPath)
        return
    
    for image in os.listdir(dirPath):
        imagePath = os.path.join(dirPath, image)
        if "Store" in image:
            continue
        m = re.findall(r"\d+$", os.path.splitext(image)[0])
        iNumber = int(m[0])
        newName = imageBase.format(cNumber, iNumber)
        #print imagePath, newName
        os.rename(imagePath, newName)

for filename in os.listdir(base):
    if os.path.isdir(os.path.join(base, filename)):
        fixDir(filename)
