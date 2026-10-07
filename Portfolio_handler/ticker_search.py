import yfinance as yf

'''USES YAHOO API TO SEARCH FOR TICKER'''
def tickerSearch(company):
    results = yf.Search(company)
    ticker = results.quotes[0]['symbol']
    #returns Ticker 
    return ticker