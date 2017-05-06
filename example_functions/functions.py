def post_list(postIdDict):
    postHyperLink = []
    for item in sorted(postIdDict, key=lambda x: postIdDict[x][1]['post_date'], reverse=True):
        postHyperLink.append('* ['+postIdDict[item][1]['post_title']+']'+'('+postIdDict[item][0]+')')
    postHyperLink = '\n'.join(postHyperLink)
    return postHyperLink
