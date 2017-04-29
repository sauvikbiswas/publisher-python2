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
                    postVars['post_date'], postVars['post_title'])
    return postIdDict

def postList(postIdDict):
    postHyperLink = []
    for item in sorted(postIdDict, key=lambda x: postIdDict[x][1], reverse=True):
        postHyperLink.append('* ['+postIdDict[item][2]+']'+'('+postIdDict[item][0]+')')
    postHyperLink = '\n'.join(postHyperLink)
    return postHyperLink

postIdDict = scanVariables(folder)
extraVars = {}
extraVars['post_list'] = postList(postIdDict)
for root, dirs, files in os.walk(postFolder):
    for filename in files:
        data, var = parse.generatePost(folder, filename, postIdDict, extraVars)
        print filename.replace('.md','.html')
        writeFile(htmlFolder, filename.replace('.md','.html'), data)
