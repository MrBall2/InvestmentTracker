import yfinance as yf
import newspaper
from ollama import chat



#Retrieves article link
#Two searches just in case one doesn't provide anything
ticker = 'XLK'
data = yf.Search(f"{ticker} stock", news_count=5).news
data2 = yf.Search(f'{ticker}', news_count=5).news


'''ARTICLE SELECTION TEST'''
#lists for titles the AI can pick from to read
titleList = []

#Goes through search results adding them to the list
for article in data:
    #Checks if "article" is a story (rather than video)
    if article['type'] == 'STORY':
        link = article['link']
        title = article['title']
        titleList.append(title)
        #x = newspaper.article(link)
        #print(x)
for article in data2:
    #Checks if "article" is a story (rather than video)
    if article['type'] == 'STORY':
        link = article['link']
        title = article['title']
        titleList.append(title)
        #x = newspaper.article(link)
        #print(x)

#Displays titles from search results
for title in titleList:
    print()
    print(f'- {title}')
print()
message = f'Based on these titles: {titleList}. Which would you choose to read if you had to make a monthly report on {ticker} Stocks?'
print(message) 
print()
response = chat(
    model = 'qwen3', #8b model
    messages = [{'role':'user', 'content':f'Based on these titles: {titleList}. Which would you choose to read if you had to make a monthly report on {ticker} Stocks?'}]
)




'''SUMMARY TEST'''
# link = data2[0]['link']
# title = data2[0]['title']
# article = newspaper.article(link)
# print(title)
# print(link)
# response = chat(
#     model = 'qwen3',
#     messages = [{'role':'user', 'content':f'Summarize this article: {article}'}]
# )


print(response.message.content)

