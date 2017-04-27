from pprint import pprint as pp
import re

varDeclareRe = re.compile('^\s*\$\s*(\w+)\s*:\s*(.*)')
# varDeclareRe = re.compile('^\s*\$')

def parseVars(data):
    for line in data:
        match = varDeclareRe.search(line)
        if match:
            print match.group(1), ':', match.group(2)
            flag = True

def readFile(filename):
    ''' Reads a markdown file and returns a list of strings '''
    with open(filename, 'rU') as fppost:
        data = fppost.read().split('\n')
    return data


data = readFile('my_blog/header.md') + \
    readFile('my_blog/posts/2017-04-27-whoami.md')


parseVars(data)
