import os
import sys
import parse
from functions import post_list

folder = sys.argv[1]

postFolder = os.path.join(folder,'posts')
htmlFolder = os.path.join(folder,'html')

def writeFile(folder, filename, data):
    if not os.path.isdir(folder):
        os.mkdir(folder)
    with open(os.path.join(folder,filename), 'wb') as fpout:
        fpout.write(data)
    return

def scanVariables(folder):
    postIdDict = {}
    for root, dirs, files in os.walk(os.path.join(folder, 'posts')):
        for filename in files:
            postFile = os.path.join(folder, 'posts', filename)
            data = parse.readFile(postFile)
            _, postVars = parse.parseVars(data, removeVars=False)
            if 'post_id' in postVars:
                postIdDict[postVars['post_id']] = (filename.replace('.md','.html'),
                    postVars)
    return postIdDict

functionRepo = parse.scanFunctions(folder)
postIdDict = scanVariables(folder)
extraVars = {}
for functionName in functionRepo:
    extraVars[functionName] = functionRepo[functionName](postIdDict)
    
for root, dirs, files in os.walk(postFolder):
    for filename in files:
        data, var = parse.generatePost(folder, filename, postIdDict, extraVars)
        print filename.replace('.md','.html')
        writeFile(htmlFolder, filename.replace('.md','.html'), data)
