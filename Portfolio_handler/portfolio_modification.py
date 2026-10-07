from .ticker_search import tickerSearch
from .calculations import *
import yfinance as yf

'''HANDLES PORTFOLIO CREATION'''
def portfolioCreation():
    data = {}
    while True:
        #Asks user for company
        company = input("Enter Company or Ticker:\t")
        ticker = tickerSearch(company)
        #adds userdata list with ticker name as value
        data[ticker] = userData(ticker)
        #checks if user is done
        check = input("Enter another company?(y/n) \t").lower()
        print('--------------------------')
        if check == 'n':
            break
    print(data)
    #Returns dictionary
    return data    

#Collects investment data from user and current stock price and puts it in a list
def userData(ticker):
    tickerData = []
    stock = yf.Ticker(ticker)
    invested = round(float(input("How much do you have invested?\t")),2)
    profit = round(float(input(f"What is the total profit/loss for {ticker}?\t")),2) #I'll use this to get percentages later
    profitPercentage = round((profit/(invested - profit))*100,2)  #profit/raw value --> percentage gain

    #Adds current price of stock
    tickerData.append(stock.fast_info['lastPrice'])#Stock Value (0)
    tickerData.append(profit) #Profit (1)
    tickerData.append(invested) #Amount invested (2)
    tickerData.append(profitPercentage) #Profit % (3)
    
    #returns list: [Value, Profit, amount invested, profit%]
    return tickerData

'''HANDLES MONTHLY UPDATES'''
#Updates investment values (monthly update)
def updateData(data):
    for stock in data:
        currentValue = data[stock][0] #Gets the value of stock
        currentAmount = data[stock][2] #Gets the amount invested
        #Creates Ticker for data collection
        s = yf.Ticker(stock)
        tempValue = s.fast_info['lastPrice'] #Gets updated value of stock
        percentGain = ((tempValue - currentValue)/currentValue) #Percent that the stock has increased since last update
        gain = currentAmount * percentGain
        #Finalize updates
        data[stock][2] += gain #AMOUNT INVESTED (former amount + (former * %gain))
        data[stock][1] += gain #PROFIT (Updated amount invested - former amount invested)
        data[stock][3] = round((data[stock][1]/(data[stock][2] - data[stock][1]))*100,2) #PROFIT % (profit/(profit-current invested))
        data[stock][0] = tempValue #STOCK VALUE

    return data

'''HANDLES ADDING AND REMOVING STOCKS FROM PORTFOLIO'''
def updatePortfolio(data):
    print("Which stock would you like to update?")
    names = list(data.keys())
    for i in range(len(names)):
        print(f'{i}: {names[i]}')
    print(f'{len(names)}: Add Stock...')

    selection = int(input('Enter number:\t'))
    if selection < len(names):
        #Buying or selling stocks
        updateStock(data,names[selection]) #name[selection] is the ticker
    else:
        #Adding new stocks to portfolio
        company = input("Enter Company or Ticker:\t")
        ticker = tickerSearch(company) #Company ticker
        newCompany = userData(ticker) #List of user stats for new Company
        data[ticker] = newCompany #adds new investment to portfolio
    print('--------------------------')
    return data

#Either changes amount invested or deletes stock from portfolio
def updateStock(data,ticker):
    print('--------------------------')
    choice = input("What would you like to update\n0: Amount Invested\n1: Delete stock\nEnter number:\t")
    match choice:
        case '0':
            #Asks if user bought or sold
            while True:
                change = input("Did you buy or sell (b/s)?\t").lower()
                match change:
                    case 'b':
                        buying(data,ticker)
                        break
                    case 's':
                        selling(data,ticker)
                        break
                    case _:
                        print("Yo pay attention...")
        case '1':
            certainty = input("Are you sure!?!?! (y/n):\t").lower()
            match certainty:
                case 'y':
                    del data[ticker] #Deletes stock from data
