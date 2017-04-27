from pprint import pprint as pp
import re

varDeclareRe = re.compile('^\s*\$\s*(\w+)\s*:\s*(.*)')
emptyLineRe = re.compile('^\s*$')
varSubstituteRe = re.compile('\'\((\w+)\)')

def parseVars(data):
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

def substituteVars(modData, postVars):
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
        subData.append(newLine)
    return subData

def readFile(filename):
    ''' Reads a markdown file and returns a list of strings '''
    with open(filename, 'rU') as fppost:
        data = fppost.read().split('\n')
    return data


data = readFile('my_blog/header.md') + \
    readFile('my_blog/posts/2017-04-27-whoami.md')


modData, postVars = parseVars(data)
pp(substituteVars(modData, postVars))
