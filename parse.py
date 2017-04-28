import re
from markdown import markdown
import os

varDeclareRe = re.compile('^\s*\$\s*(\w+)\s*:\s*(.*)')
emptyLineRe = re.compile('^\s*$')
varSubstituteRe = re.compile('\'\((\w+)\)')
linkRe = re.compile('(\[.*?\]\()(.*?)(\))')

def parseVars(data):
    ''' Parses the data to find $ variable : value lines. Removes such lines
    from data and creates a dictionary of variable -> value pairs. All empty
    lines following the $ lines are also removed '''

    modData = []
    postVars = {}
    flagFill = True
    for line in data:
        match = varDeclareRe.search(line)
        if match:
            postVars[match.group(1)] = match.group(2)
            flagFill = False
        else:
            if not flagFill:
                match = emptyLineRe.search(line)
                if not match:
                    flagFill = True
            if flagFill:
                modData.append(line)
    return modData, postVars

def substituteVars(modData, postVars, postIdDict={}):
    ''' Given a dictionary or variable -> value pairs (postVars), it takes
    modData and substitutes all occurances of '(variable) to corresponding
    values '''

    subData = []
    for line in modData:
        newLine = line

        match = varSubstituteRe.findall(line)
        replacementSet = set(match)
        removalSet = set([])
        for item in replacementSet:
            if item not in postVars:
                removalSet.add(item)
        replacementSet = replacementSet - removalSet
        for item in replacementSet:
            newLine = newLine.replace('\'('+item+')', postVars[item])

        matchiter = linkRe.finditer(newLine)
        replacementDict = {}
        for match in matchiter:
            postId = match.group(2)
            if postId in postIdDict:
                replacementDict[match.group(0)] = match.group(1) + \
                    postIdDict[postId][0] + match.group(3)

        for postIdLink in replacementDict:
            newLine = newLine.replace(postIdLink, replacementDict[postIdLink])

        subData.append(newLine)
    return subData

def readFile(filename):
    ''' Reads a markdown file and returns a list of strings '''
    data = []
    if os.path.isfile(filename):
        with open(filename, 'rU') as fppost:
            data = fppost.read().strip().split('\n')
    return data

def generatePost(folder, postFile, postIdDict = {}, postVarsExtra={}):
    ''' Given the blog folder and the postfile in posts, generates a complete
    HTML file. No markdown transformation is applied to the header and footer
    '''

    headerFile = os.path.join(folder,'header.html')
    footerFile = os.path.join(folder,'footer.html')
    postFile = os.path.join(folder, 'posts', postFile)

    datalist = [readFile(headerFile),
                readFile(postFile),
                readFile(footerFile)]

    data = reduce(lambda x, y: x+y, datalist)

    modData, postVars = parseVars(data)
    postVars.update(postVarsExtra)
    mdData = substituteVars(modData, postVars, postIdDict)
    postHTMLData = '\n'.join([
        '\n'.join(mdData[:len(datalist[0])]),
        markdown('\n'.join(mdData[len(datalist[0]):-len(datalist[2])])),
        '\n'.join(mdData[-len(datalist[2]):])
        ])

    return postHTMLData, postVars

def readPostVars(folder, postFile):
    postFile = os.path.join(folder, 'posts', postFile)
    data = readFile(postFile)
    _, postVars = parseVars(data)
    return postVars
