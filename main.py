#Imports all the necessary functions
from Portfolio_handler.csv_handler import *
from Portfolio_handler.portfolio_modification import *
from Portfolio_handler.calculations import *
from AI_summary.summary import summaryStart

def launch():
    print("Welcome...")
    while True:
        print("0: Create New Portfolio\n1: Update Current Portfolio\n2: Monthly Update\n3: Data Analysis")
        selection = input("Enter Your Selection:\t")
        print('-------------------')
        match selection:
            case '0':
                print("NEW PORTFOLIO")
                data = portfolioCreation() #Creates portfolio
                csvCreate(data) #Creates updated monthly and portfolio csv file
            case '1':
                print("UPDATE PORTFOLIO")
                data = csvData() #Gets data from monthly.csv
                data = updatePortfolio(data) #updates portfolio data
                csvCreate(data) #Creates updated monthly and portfolio csv file
            case '2':
                print("MONTHLY UPDATE")
                data = csvData() #Gets data from monthly.csv
                updateData(data) #Updates to current value
                csvCreate(data) #Creates updated monthly and portfolio csv file
            case '3':
                print("DATA ANALYSIS")
                currentData = csvData()
                priorData = csvPriorData()
                summaryStart(priorData,currentData)

            case _:
                print('Invalid...')
        if input('Done (y/n)?\t') == 'y':
            print("Bye Bye...")
            break

#main
launch()

#TICKER: [Value, Profit, Amount Invested, Profit%] 