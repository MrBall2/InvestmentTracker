#Returns article
import newspaper


def article_select(titleDict, title):
    link = titleDict[title][0]
    article = newspaper.article(link)
    return article


#Let's the AI return a tool call that gives the article's title
ARTICLE_SELECT = {
    'type': 'function',
    'function': {
        'name':'article_select',
        'description': '''
        Use this tool to get an article you choose to read based on its title. Only one title can be chosen at a time.
        ''',

        'parameters':{
            'type': 'object',
            'properties':{
                'message':{
                    'types':'string',
                    'description': 'The title for the most relevant article.'
                }
            },
            'required':['message'],
            'additionalProperties': False
        }
    }
}