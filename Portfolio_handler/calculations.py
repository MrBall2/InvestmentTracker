#Calculations when selling stock
def selling(data,ticker):
    priceChange = float(input("Enter amount sold: $"))

    #Profit Changes because you sold off some of that profit
    profitPercentage = data[ticker][3] / 100
    realizedGain = priceChange * profitPercentage #Amount of profit that was sold off
    data[ticker][1] -= realizedGain #Subtracts realized gain from profit (New profit #)

    #Amount that remains after selling
    data[ticker][2] -= priceChange #amount invested goes down by what you sold

#Calculations when buying stock
def buying(data,ticker):
    print(data)
    profit = data[ticker][1]
    priceChange = float(input("Enter amount bought: $"))
    data[ticker][2] += priceChange #amount invested goes up
    data[ticker][3] = round((profit/data[ticker][2]) * 100,2) #Profit % update
    print(data)