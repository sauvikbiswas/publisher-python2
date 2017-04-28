import os
import sys
import parse

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
            postVars = parse.readPostVars(folder, filename)
            if 'post_id' in postVars:
                postIdDict[postVars['post_id']] = (filename.replace('.md','.html'),
                    postVars['post_date'])
    return postIdDict

postIdDict = scanVariables(folder)
print postIdDict
for root, dirs, files in os.walk(postFolder):
    for filename in files:
        data, var = parse.generatePost(folder, filename, postIdDict)
        writeFile(htmlFolder, filename.replace('.md','.html'), data)
