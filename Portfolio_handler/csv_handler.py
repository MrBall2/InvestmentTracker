import pandas as pd
from time import strftime

'''HANDLES CSV FILES'''
def csvCreate(data):
    
    csvPriorMonth()

    month = strftime("%B") #Gets current month
    #Sets up CSV file
    df = pd.DataFrame(data, index=['Value', 'Gain/Loss','Amount Invested', 'percentGain']).T    #"T" flips rows and columns
    #df = df.drop(columns=['percentGain']) #I don't have it in my spreadsheets rn but it might be useful info
    df.index.name = month

    #Exports csv file
    df.to_csv('Portfolio_handler/monthly.csv') #This one makes it easy to download and paste into google sheets

    try:
        existing = pd.read_csv('Portfolio_handler/portfolio.csv', index_col = 0) #reads existing portfolio file
        updated = pd.concat([existing,df]) #attaches new data
        updated.to_csv('Portfolio_handler/portfolio.csv')

    except (FileNotFoundError, pd.errors.EmptyDataError):
        df.to_csv('Portfolio_handler/portfolio.csv')
    #Displays table
    print(df)
    print('--------------------------')


#Gets data from former csv file
def csvData():
    df = pd.read_csv('Portfolio_handler/monthly.csv',index_col=0)
    data = {ticker: list(row) for ticker, row in df.iterrows()} #Creates a dictionary based on monthly.csv
    return data


#PRIOR MONTH DATA HANDLING
def csvPriorMonth():
    try:
        existing = pd.read_csv('Portfolio_handler/monthly.csv', index_col = 0)
        existing.to_csv('Portfolio_handler/priorMonth.csv')
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return

def csvPriorData():
    df = pd.read_csv('Portfolio_handler/priorMonth.csv',index_col=0)
    data = {ticker: list(row) for ticker, row in df.iterrows()} #Creates a dictionary based on monthly.csv
    return data