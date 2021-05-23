import os
import sys
import parse
from functions import post_list

folder = sys.argv[1]

postFolder = os.path.join(folder,'posts')
htmlFolder = os.path.join(folder,'temp')

def writeFile(folder, filename, data):
    if not os.path.isdir(folder):
        os.mkdir(folder)
    with open(os.path.join(folder,filename), 'wb') as fpout:
        fpout.write(data)
    return

def scanVariables(folder):
    postIdDictPreLink = {}
    postIdDict = {}
    for root, dirs, files in os.walk(postFolder):
        for filename in files:
            postFile = os.path.join(folder, 'posts', filename)
            data = parse.readFile(postFile)
            _, postVars = parse.parseVars(data, removeVars=False)
            if 'post_id' in postVars:
                postIdDictPreLink[postVars['post_id']] = (filename.replace('.md','.html'),
                    postVars)

    # Auxiliary set of variables for links (i.e. _<post_id> = <filename>)
    fileLinkDict = {}
    for post_id in postIdDictPreLink:
        filename, _ = postIdDictPreLink[post_id]
        fileLinkDict['@'+post_id] = filename
    for post_id in postIdDictPreLink:
        filename, postVars = postIdDictPreLink[post_id]
        postVars.update(fileLinkDict)
        postIdDict[post_id] = (filename, postVars)

    return postIdDict

functionRepo = parse.scanFunctions(folder)
postIdDict = scanVariables(folder)
extraVars = {}
for functionName in functionRepo:
    extraVars[functionName] = functionRepo[functionName](postIdDict)

print "Generating Posts"
for root, dirs, files in os.walk(postFolder):
    for filename in files:
        data, var = parse.generatePost(folder, filename, postIdDict, extraVars)
        print "\t"+filename.replace('.md','.html')
        writeFile(htmlFolder, filename.replace('.md','.html'), data)
