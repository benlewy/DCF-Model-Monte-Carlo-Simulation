import yfinance as yf
import matplotlib.pyplot as plt
import random

userInput = str(input("Enter ticker you wish to value ")).upper()  # asks user for input

stock = yf.Ticker(userInput)  # grabs the ticker
outstandingShares = stock.info['sharesOutstanding']  # fetches number of outstanding shares

# free cash flow inputs
cashMinusOne = int(input("Enter the free cash flow from previous year (1000s of $) "))
cashMinusTwo = int(input("Enter the free cash flow from two years ago (1000s of $) "))
cashMinusThree = int(input("Enter the free cash flow from three years ago (1000s of $) "))
cashMinusFour = int(input("Enter the free cash flow from four years ago (1000s of $) "))

input('Press Enter to Continue with Valuation')

simDistribution = []
numSims = 10000

for i in range(numSims):

    requiredRate = random.uniform(0.00, 0.10)
    perpetualRate = random.uniform(0.00, 0.05)
    cashflowGrowthRate = random.uniform(0.00, 0.05)

    years = [1, 2, 3, 4]

    freeCashflow = [cashMinusOne, cashMinusTwo, cashMinusThree, cashMinusFour]

    # DCF calculations using inputs from above
    futureFreeCashflow = []
    discountFactor = []
    discountedFutureFreeCashflow = []

    terminalValue = freeCashflow[0] * (1 + perpetualRate) / (requiredRate - perpetualRate)

    for year in years:
        cashflow = freeCashflow[0] * (1 + cashflowGrowthRate) ** year
        futureFreeCashflow.append(cashflow)
        discountFactor.append((1 + requiredRate) ** year)

    for z in range(0, len(years)):
        discountedFutureFreeCashflow.append(futureFreeCashflow[z] / discountFactor[z])

    discountedTerminalValue = terminalValue / (1 + requiredRate) ** (len(years))
    discountedFutureFreeCashflow.append(discountedTerminalValue)

    currentValue = sum(discountedFutureFreeCashflow)

    fairValue = ((currentValue * 1000) / outstandingShares)

    simDistribution.append(fairValue)

simDistributionS = sum(simDistribution)
simDistributionL = len(simDistribution)
meanSimDistribution = simDistributionS / simDistributionL
print(f"The Average Simulated Price is ${meanSimDistribution}")

# plot histogram
plt.hist(simDistribution, bins=350, range=[0, 350])
plt.axvline(meanSimDistribution, color='k', linestyle='dashed', linewidth=1)
plt.title('Simulation of DCF Values')
plt.xlabel('Fair Value Price')
plt.ylabel('Fair Value Density')
plt.show()