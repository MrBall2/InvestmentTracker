from ollama import chat, web_search, web_fetch
import yfinance as yf
from .tools import ARTICLE_SELECT, article_select


#Gets titles of articles based on tickers
def titles(ticker):

    data = yf.Search(f"{ticker} stock", news_count=5).news
    data2 = yf.Search(f'{ticker}', news_count=5).news


    '''Finds articles'''
    #lists for titles the AI can pick from to read
    titleDict = {}
    #Goes through search results adding them to the list
    for article in data:
        #Checks if "article" is a story (rather than video)
        if article['type'] == 'STORY':
            link = article['link']
            title = article['title']
            #Adds title as key and link as value
            titleDict[title] = [link]
    for article in data2:
        #Checks if "article" is a story (rather than video)
        if article['type'] == 'STORY':
            link = article['link']
            title = article['title']
            #Adds title as key and link as value
            titleDict[title] = [link]

    #for title in titleDict: print('-',title), print()
    #returns list of titles
    return titleDict


#looks for tool calls from AI response then finds article based on selected
def toolResponse(response,messages,titleDict):

    if response.message.tool_calls:
        messages.append(response.message)
        for tool in response.message.tool_calls:
            #print(titleDict.keys())
            #print(tool)
            #AI's inquery
            title = tool.function.arguments['message']
            print(f'Pulling Article: {title}')
            article = article_select(titleDict,title)
            print('Article found...')

            #Add model's response and tool result to messages (adds onto message history basically)
            messages.append({
                'role':'tool',
                'content':str(article)
            })

    return messages

#Creates AI summary
def aiSummary(ticker, titleDict, priorMonth, currentMonth):
    titleList = list(titleDict) #A list of only titles to make it easier for the AI (titleDict also includes links)
    print('understood...')

    #Initial prompt asking it to pick an article to read.
    messages = [
            {
                'role':'system',
                'content': 'You are a financial analyst. Analyze stock performance based on recent news. '
            },
            {
                'role':'user',
                'content':f'''
                The following lists include {ticker} share value($), user's profit($), and total amount invested in the stock($).
                This is the information for the prior month: {priorMonth}.
                This is the information for the current month: {currentMonth}.

                You must provide reasoning for why the {ticker} stock performed the way it did this past month. 
                Select up to three articles that will best aid you in making this analysis. 
                Here is a list of article titles to choose from: {titleList}.
                '''
            }
        ]
    titleSelect = chat(model = 'qwen3', messages = messages, tools = [ARTICLE_SELECT])
    print('Titles selected...')
    #print(titleSelect.message.thinking)
    print()
    #Finds article, appends it to messages, returns messages
    messages = toolResponse(titleSelect,messages,titleDict)

    #Secondary prompt asking for summary of articles and analysis of investments
    messages.append({
        'role':'user',
        'content': f'''
        Using the articles provided give a summary of {ticker} stocks.
        Provide a potential explanation for the stock's performance this past month based on the user data provided initially.
        '''
    })
    summary = chat(model = 'qwen3', messages=messages)


    #prints results
    print()
    print(summary.message.content)

def summaryStart(priorData, currentDdata):
    #Goes through stocks you have
    print("Which stock would you like to analyze?")
    names = list(currentDdata.keys())
    for i in range(len(names)):
        print(f'{i}: {names[i]}')
    selection = int(input('Enter number:\t'))
    ticker = names[selection]
    #Starts summary process
    titleDict = titles(ticker)
    aiSummary(ticker,titleDict,priorData,currentDdata)
