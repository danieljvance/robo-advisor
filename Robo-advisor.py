# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 14:12:43 2020

@author: Daniel Vance
"""
import tkinter as tk
import pandas as pd
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
from pandas_datareader import data
import numpy as np
import statistics as stats # need this to take standard deviations
from random import choice # choice will select an item from list at random
#import matplotlib.pyplot as plt
from tkinter import simpledialog

root = tk.Tk()
   

stocks = pd.read_csv('Stocks.csv', index_col = "Categories")
comm = pd.read_csv('Curr.csv', index_col = "Categories")
bonds = pd.read_csv('Bond.csv', index_col = "Categories")
funds = pd.read_csv('Fund.csv', index_col = "Categories")


risk_assesment = tk.IntVar()


Tech = tk.IntVar()
ConSt = tk.IntVar()
Health = tk.IntVar()
Energy = tk.IntVar() 
FinServ = tk.IntVar()
stocksInd=[]
bondsInd = []

stockChoice = tk.IntVar()
bondChoice = tk.IntVar()
fundChoice = tk.IntVar()
commChoice = tk.IntVar() 

# Checkboxes for industry preferences--------------------------
tk.Label(root, text="Industry Focus (Select all that apply): ").grid(row=0, column=0)
tk.Checkbutton(root, text="Tech", variable=Tech).grid(row=1, column=0)
tk.Checkbutton(root, text="Consumer Staples", variable=ConSt).grid(row=2, column=0)
tk.Checkbutton(root, text="Energy", variable=Energy).grid(row=3, column=0)
tk.Checkbutton(root, text="Financial Services", variable=FinServ).grid(row=4, column=0)
tk.Checkbutton(root, text="Healthcare", variable=Health).grid(row=5, column=0)

# Checkboxes for asset class preferences-------------------------------------
tk.Label(root, text="Asset Class Exclusions (Select one at most): ").grid(row=7, column=0)
tk.Checkbutton(root, text="Equity", variable=stockChoice).grid(row=8, column=0)
tk.Checkbutton(root, text="Bond", variable=bondChoice).grid(row=9, column=0)
tk.Checkbutton(root, text="Fund", variable=fundChoice).grid(row=10, column=0)
tk.Checkbutton(root, text="Currencies", variable=commChoice).grid(row=11, column=0)

# Liquidity selection
tk.Label(root, text="Do you require liquidity? ").grid(row=13, column=0)
liquidityChoice = tk.StringVar()
liquidityChoice.set("No")
liquidityOpt = tk.OptionMenu(root, liquidityChoice, "Yes", "No")
liquidityOpt.grid(row=14, column=0)

alloAmount = int(simpledialog.askstring(title="Investment Amount.", prompt = "Enter amount to invest." ))

## Question 1
#------------------------------------------------------------------------------- 
#setting up variable 1 (time horizon)

q1Choice = tk.StringVar()

answers1 =[
        "18-30",
        "31-50",
        "51+"
]

# setting up answer text
q1Choice.set("18-30")
 
# setting up question 1 (time horizon)
tk.Label(root,
         text="Q1: What is your age?", 
         wraplength=900,
         ).grid(row=0, column=1, sticky=tk.W, padx=20, pady=5)
option1 = tk.OptionMenu(root, q1Choice, *answers1)
option1.grid(row=1, column=1, sticky=tk.W, padx=20, pady=5)

## Question 2
#------------------------------------------------------------------------------- 
#setting up variable 2 (time horizon)

q2Choice = tk.StringVar()

answers2 = [
        "1-3 Years",
        "3-5 Years",
        "5+ Years"
]

# setting up answer text
q2Choice.set("1-3 Years")

# setting up question 2 (time horizon)
tk.Label(root,
         text="Q2: How long do you plan to stay invested?",
         wraplength=900,
         ).grid(row=2, column=1,sticky=tk.W, padx=20, pady=5)
option2 = tk.OptionMenu(root, q2Choice, *answers2)
option2.grid(row=3, column=1, sticky=tk.W, padx=20, pady=5)

## Question 3
#------------------------------------------------------------------------------- 
#setting up variable 3 (risk aversion)

q3Choice = tk.StringVar()


answers3 = [
        "less than $50,000",
        "$50,000 - $150,000",
        "more than $150,000",
]

# setting up answer text
q3Choice.set("less than $50,000")

# setting up question 3
tk.Label(root,
         text="Q3: What is your annual income?",
         wraplength=900,
         ).grid(row=4, column=1,sticky=tk.W, padx=20, pady=5 )
option3 = tk.OptionMenu(root, q3Choice, *answers3)
option3.grid(row=5, column=1, sticky=tk.W, padx=20, pady=5)

## Question 4    
#------------------------------------------------------------------------------- 
    
#setting up variable 4 (risk aversion)
q4Choice = tk.StringVar()

answers4 = [
        "Unstable",
        "Moderately Stable",
        "Very Stable"
]
# setting up answer text
q4Choice.set("Unstable")
 
# setting up question 4 
tk.Label(root,
         text="Q4: Rate the stability of your income.",
         wraplength=900,
         justify = tk.LEFT
         ).grid(row=6, column=1,sticky=tk.W, padx=20, pady=5)
option4 = tk.OptionMenu(root, q4Choice, *answers4)
option4.grid(row=7, column=1, sticky=tk.W, padx=20, pady=5)

## Question 5
#------------------------------------------------------------------------------- 
    
#setting up variable 5 (risk aversion)
q5Choice = tk.StringVar()

answers5 = [
        "None",
        "Limited",
        "Good"
]

# setting up answer text
q5Choice.set("None")

# setting up question 5 
tk.Label(root,
         text="Q5: How would you describe your knowledge of investments?",
         wraplength=900,
         ).grid(row=8, column=1,sticky=tk.W, padx=20, pady=5)
option5 = tk.OptionMenu(root, q5Choice, *answers5)
option5.grid(row=9, column=1, sticky=tk.W, padx=20, pady=5)

## Question 6  
#------------------------------------------------------------------------------- 

#setting up variable 6 (risk aversion)
q6Choice = tk.StringVar()

answers6 = [
        "Investments losing value",
        "Losing/gaining value equally",
        "Investments gaining value",
]

# setting up answer text
q6Choice.set("Investments losing value")

# setting up question 6 
tk.Label(root,
         text="Q6: When investing money you are most concerned about:",
         wraplength=900,
         justify = tk.LEFT
         ).grid(row=10, column=1,sticky=tk.W, padx=20, pady=5)
option6 = tk.OptionMenu(root, q6Choice, *answers6)
option6.grid(row=11, column=1, sticky=tk.W, padx=20, pady=5)

## Question 7
#------------------------------------------------------------------------------- 
#setting up variable 7 (risk aversion)
q7Choice = tk.StringVar()

answers7 = [
        "Sell shares",
        "Do nothing",
        "Buy more shares"
]

# setting up answer text
q7Choice.set("Sell shares")
    
# setting up question 7 
tk.Label(root,
         text="Q7: Imagine that in the past three months, the overall stock market lost 25% of its value. An individual stock investment you own also lost 25% of its value. What would you do?",
         wraplength=900,
         ).grid(row=12, column=1,sticky=tk.W, padx=20, pady=5)
option7 = tk.OptionMenu(root, q7Choice, *answers7)
option7.grid(row=13, column=1, sticky=tk.W, padx=20, pady=5)


## Question 8
#-------------------------------------------------------------------------------    
#setting up variable 8 (risk aversion)
q8Choice= tk.StringVar()

answers8 = [
        "Minimize risk while aiming for maximum returns",
        "Return is equally as important as risk of losses",
        "Maximize returns",

]

# setting up answer text
q8Choice.set("Minimize risk while aiming for maximum returns")

# setting up question 8
tk.Label(root,
         text="Q8: Investing involves a trade-off between risk and return. What are your priorities for your retirement savings?",
         wraplength=900,
         ).grid(row=14, column=1,sticky=tk.W, padx=20, pady=5)
option8 = tk.OptionMenu(root, q8Choice, *answers8)
option8.grid(row=15, column=1, sticky=tk.W, padx=20, pady=5)
 

## END OF QUESTIONNARIE 
#------------------------------------------------------------------------------- 
  

def price_tickers (tickers, start):
    stock_data = data.DataReader(tickers, data_source = 'yahoo', start=start)['Adj Close']
    
    return stock_data


def CalculateProfile ():
    
    stocksFinal=[]
    commFinal = []
    bondsFinal = []
    fundFinal = []
    
    ## Stock Sorting--------------------------------------    
    if Tech.get() == 1 :
        for i in range(0,98):
            if stocks.iat[2, i] == "Tech":
                if stocks.iat[0,i] not in stocksInd :
                    stocksInd.append(stocks.iat[0,i])

    if ConSt.get() == 1 :
        for i in range(0,98):
            if stocks.iat[2, i] == "Consumer Staples":
                if stocks.iat[0,i] not in stocksInd :
                    stocksInd.append(stocks.iat[0,i])

    if FinServ.get() == 1 :
        for i in range(0,98):
            if stocks.iat[2, i] == "Financial Services":
                if stocks.iat[0,i] not in stocksInd :
                    stocksInd.append(stocks.iat[0,i])

    if Energy.get() == 1 :
        for i in range(0,98):
            if stocks.iat[2, i] == "Energy":
                if stocks.iat[0,i] not in stocksInd :
                    stocksInd.append(stocks.iat[0,i])

    if Health.get() == 1 :
        for i in range(0,98):
            if stocks.iat[2, i] == "Healthcare":
                if stocks.iat[0,i] not in stocksInd :
                    stocksInd.append(stocks.iat[0,i])
                        
                        
    if liquidityChoice.get() == "Yes" :
        for i in range(0,98):
            if stocks.iat[3, i] == "Y":
                if stocks.iat[0,i] in stocksInd :
                    stocksFinal.append(stocks.iat[0,i])

    elif liquidityChoice.get() == "No" :
        stocksFinal = stocksInd
       
        
        
    ## Commodity Sorting-----------------------------------
    for i in range(0,10):
        commFinal.append(comm.iat[0,i])
       
        
        
    ## Bond Sorting--------------------------------------    
    if Tech.get() == 1 :
        for i in range(0,20):
            if bonds.iat[2, i] == "Tech":
                if bonds.iat[0,i] not in bondsInd :
                    bondsInd.append(bonds.iat[0,i])

    if ConSt.get() == 1 :
        for i in range(0,20):
            if bonds.iat[2, i] == "Consumer Staples":
                if bonds.iat[0,i] not in bondsInd :
                    bondsInd.append(bonds.iat[0,i])

    if FinServ.get() == 1 :
        for i in range(0,20):
            if bonds.iat[2, i] == "Financial Services":
                if bonds.iat[0,i] not in bondsInd :
                    bondsInd.append(bonds.iat[0,i])

    if Energy.get() == 1 :
        for i in range(0,20):
            if bonds.iat[2, i] == "Energy":
                if bonds.iat[0,i] not in bondsInd :
                    bondsInd.append(bonds.iat[0,i])

    if Health.get() == 1 :
        for i in range(0,20):
            if bonds.iat[2, i] == "Healthcare":
                if bonds.iat[0,i] not in bondsInd :
                    bondsInd.append(bonds.iat[0,i])
                        
                        
    if liquidityChoice.get() == "Yes" :
        for i in range(0,20):
            if bonds.iat[3, i] == "Y":
                if bonds.iat[0,i] in bondsInd :
                    bondsFinal.append(bonds.iat[0,i])
    elif liquidityChoice.get() == "No" :
        bondsFinal = bondsInd
        
        
        
    ## Fund Sorting (Need to pull in the 5 extra then sort the industry indeces)

    if Tech.get() == 1 :
        for i in range(0,7):
            if funds.iat[2, i] == "Tech":
                if bonds.iat[0,i] not in fundFinal :
                    fundFinal.append(funds.iat[0,i])


    if ConSt.get() == 1 :
        for i in range(0,7):
            if funds.iat[2, i] == "Consumer Staples":
                if bonds.iat[0,i] not in fundFinal :
                    fundFinal.append(funds.iat[0,i])

    if FinServ.get() == 1 :
        for i in range(0,7):
            if funds.iat[2, i] == "Financial Services":
                if bonds.iat[0,i] not in fundFinal :
                    fundFinal.append(funds.iat[0,i])

    if Energy.get() == 1 :
        for i in range(0,7):
            if funds.iat[2, i] == "Energy":
                if bonds.iat[0,i] not in fundFinal :
                    fundFinal.append(funds.iat[0,i])

    if Health.get() == 1 :
        for i in range(0,7):
            if funds.iat[2, i] == "Healthcare":
                if bonds.iat[0,i] not in fundFinal :
                    fundFinal.append(funds.iat[0,i])      
     
        
    print(stocksFinal)
    print(bondsFinal)
    print(commFinal)
    print(fundFinal)
    
    ## Setting up an investment profile- percentage [Stocks, Bonds, Currencies, Funds]
    Conservative_all = [.10, .50, .10, .30]
    Conservative_noFund = [.10, .80, .10, 0]
    Conservative_noComm = [.10, .80, 0, .10]
    Conservative_noBond = [.10, 0, .20, .70]
    Conservative_noEquity =[0, .80, .10, .10]
    ModeratelyConservative_all = [.20, .40, .15, .25]
    ModeratelyConservative_noFund = [.15, .70, .15, 0]
    ModeratelyConservative_noComm = [.10, .70, 0, .20]
    ModeratelyConservative_noBond = [.15, 0, .20, .65]
    ModeratelyConservative_noEquity = [0, .75, .10, .15]
    Moderate_all = [.30, .25, .20, .25]
    Moderate_noFund = [.35, .30, .35, 0]
    Moderate_noComm = [.35, .30, 0, .35]
    Moderate_noBond = [.35, 0, .30, .35]
    Moderate_noEquity = [0, .30, .35, .35]
    ModeratelyAggressive_all = [.40, .15, .25, .25]
    ModeratelyAggressive_noFund = [.50, .15, .35, 0]
    ModeratelyAggressive_noComm = [.55, .15, 0, .30]
    ModeratelyAggressive_noBond = [.55, 0, .25, .20]
    ModeratelyAggressive_noEquity = [0, .10, .40, .50]
    Aggressive_all = [.65, 0, .20, .15]
    Aggressive_noFund = [.70, 0, .30, 0]
    Aggressive_noComm = [.70, 0, 0, .30]
    Aggressive_noBond = [.70, 0, .20, .10]
    Aggressive_noEquity = [0, 0, .55, .45]
    FinalProfile = Conservative_all
    
    stockWeights_short = {}
    stockWeights_med = {}
    stockWeights_long = {}
    commWeights_short = {}
    commWeights_med = {}
    commWeights_long = {}
    bondWeights_short = {}
    bondWeights_med = {}
    bondWeights_long = {}
    fundWeights_short = {}
    fundWeights_med = {}
    fundWeights_long = {}
    
    ## END OF INVESTORS PROFILE
    q1= 0
    q2= 0
    q3= 0
    q4= 0
    q5= 0
    q6= 0
    q7= 0
    q8= 0
    
    ## Risk Value for Question 1
    if q1Choice.get() == "18-30":
        q1 = 8
    elif q1Choice.get() == "31-50":
        q1 = 5
    elif q1Choice.get() == "51+":
        q1 = 2
    
    ## Risk Value for Question 2
    if q2Choice.get() == "1-3 Years":
        q2 = 0
    elif q2Choice.get() == "3-5 Years":
        q2 = 5
    elif q2Choice.get() == "5+ Years":
        q2 = 10
    
    ## Risk Value for Question 3
    if q3Choice.get() == "less than $50,000":
        q3 = 1
    elif q3Choice.get() == "$50,000 - $150,000":
        q3 = 5
    elif q3Choice.get() == "more than $150,000":
        q3 = 10
    
    ## Risk Value for Question 4
    if q4Choice.get() == "Unstable":
        q4 = 0
    elif q4Choice.get() == "Moderately Stable":
        q4 = 4
    elif q4Choice.get() == "Very Stable":
        q4 = 8

    ## Risk Value for Question 5
    if q5Choice.get() == "None":
        q5 = 2
    elif q5Choice.get() == "Limited":
        q5 = 5
    elif q5Choice.get() == "Good":
        q5 = 9

    ## Risk Value for Question 6
    if q6Choice.get() == "Investments losing value":
        q6 = 0
    elif q6Choice.get() == "Losing/gaining value equally":
        q6 = 4
    elif q6Choice.get() == "Investments gaining value":
        q6 = 8

    ## Risk Value for Question 7
    if q7Choice.get() == "Sell shares":
        q7 = 0
    elif q7Choice.get() == "Do nothing":
        q7 = 5
    elif q7Choice.get() == "Buy more shares":
        q7 = 8  

    ## Risk Value for Question 8
    if q8Choice.get() == "Minimize risk while aiming for maximum returns":
        q8 = 1
    elif q8Choice.get() == "Return is equally as important as risk of losses":
        q8 = 5
    elif q8Choice.get() == "Maximize returns":
        q8 = 10  

    risk_assesment = q1 + q2 + q3 + q4 + q5 + q6 + q7 + q8

    print("Risk Score is: " + str(risk_assesment))
    
    
    if  6<= risk_assesment <=18 and fundChoice.get() == 1:
        FinalProfile = Conservative_noFund
    elif 6<= risk_assesment <=18 and commChoice.get() == 1 :
        FinalProfile = Conservative_noComm
    elif 6<= risk_assesment <=18 and bondChoice.get() == 1 :
        FinalProfile = Conservative_noBond
    elif 6<= risk_assesment <=18 and stockChoice.get() == 1 :
        FinalProfile = Conservative_noEquity

    if  19<= risk_assesment <=31 and fundChoice.get() == 1:
        FinalProfile = ModeratelyConservative_noFund
    elif 19<= risk_assesment <=31 and commChoice.get() == 1 :
        FinalProfile = ModeratelyConservative_noComm
    elif 19<= risk_assesment <=31 and bondChoice.get() == 1 :
        FinalProfile = ModeratelyConservative_noBond
    elif 19<= risk_assesment <=31 and stockChoice.get() == 1 :
        FinalProfile = ModeratelyConservative_noEquity
    elif 19<= risk_assesment <=31:
        FinalProfile = ModeratelyConservative_all
        
    if  32<= risk_assesment <=44 and fundChoice.get() == 1:
        FinalProfile = Moderate_noFund
    elif 32<= risk_assesment <=44 and commChoice.get() == 1 :
        FinalProfile = Moderate_noComm
    elif 32<= risk_assesment <=44 and bondChoice.get() == 1 :
        FinalProfile = Moderate_noBond
    elif 32<= risk_assesment <=44 and stockChoice.get() == 1 :
        FinalProfile = Moderate_noEquity
    elif 32<= risk_assesment <=44:
        FinalProfile = Moderate_all
        
    if  45<= risk_assesment <=57 and fundChoice.get() == 1:
        FinalProfile = ModeratelyAggressive_noFund
    elif 45<= risk_assesment <=57 and commChoice.get() == 1 :
        FinalProfile = ModeratelyAggressive_noComm
    elif 45<= risk_assesment <=57 and bondChoice.get() == 1 :
        FinalProfile = ModeratelyAggressive_noBond
    elif 45<= risk_assesment <=57 and stockChoice.get() == 1 :
        FinalProfile = ModeratelyAggressive_noEquity
    elif 45<= risk_assesment <=57:
        FinalProfile = ModeratelyAggressive_all
        
    if  58<= risk_assesment <=71 and fundChoice.get() == 1:
        FinalProfile = Aggressive_noFund
    elif 58<= risk_assesment <=71 and commChoice.get() == 1 :
        FinalProfile = Aggressive_noComm
    elif 58<= risk_assesment <=71 and bondChoice.get() == 1 :
        FinalProfile = Aggressive_noBond
    elif 58<= risk_assesment <=71 and stockChoice.get() == 1 :
        FinalProfile = Aggressive_noEquity
    elif 58<= risk_assesment <=71:
        FinalProfile = Aggressive_all


    #------------------------------------------------------------------------------- 
    ## Setting Variables for Optimimization

    startDate_short = '2019-01-01'
    startDate_med = '2017-01-01'
    startDate_long = '2015-01-01'
    risk_free_rate= 0.0154
 
### Short Analysis
    
    print("\nPortfolio for 1 year analysis beginning 1/1/2019")
## Stocks Optimization
#-------------------------------------------------------------------------------
    #get data - returns
    stocksData_short = price_tickers(stocksFinal, startDate_short)

    # Calculate expected returns and sample covariance
    stocksMu_short = expected_returns.mean_historical_return(stocksData_short)
    stocksSig_short = risk_models.sample_cov(stocksData_short)

    #Optimise each category
    stocksEF_short = EfficientFrontier(stocksMu_short, stocksSig_short)
    stockWeights_short = stocksEF_short.max_sharpe(risk_free_rate=risk_free_rate)
  
## Commodity Optimization
#-------------------------------------------------------------------------------

    commData_short = price_tickers(commFinal, startDate_short)
    
    # Calculate expected returns and sample covariance
    commMu_short = expected_returns.mean_historical_return(commData_short)
    commSig_short = risk_models.sample_cov(commData_short)

    #Optimise each category
    commEF_short = EfficientFrontier(commMu_short, commSig_short)
    commWeights_short = commEF_short.max_sharpe(risk_free_rate=risk_free_rate)

## Bond Optimization
#-------------------------------------------------------------------------------
    
    bondsData_short = price_tickers(bondsFinal, startDate_short)
    
    # Calculate expected returns and sample covariance
    bondsMu_short = expected_returns.mean_historical_return(bondsData_short)
    bondsSig_short = risk_models.sample_cov(bondsData_short)
    
    #Optimise each category
    bondsEF_short = EfficientFrontier(bondsMu_short, bondsSig_short)
    bondWeights_short = bondsEF_short.max_sharpe(risk_free_rate=risk_free_rate)

## Fund Optimization    
#-------------------------------------------------------------------------------
    
    fundData_short = price_tickers(fundFinal, startDate_short)
    
    # Calculate expected returns and sample covariance
    fundMu_short = expected_returns.mean_historical_return(fundData_short)
    fundSig_short = risk_models.sample_cov(fundData_short)

    #Optimise each category
    fundEF_short = EfficientFrontier(fundMu_short, fundSig_short)
    fundWeights_short = fundEF_short.max_sharpe(risk_free_rate=risk_free_rate)
  
    
 ## Final Portfolio
#-------------------------------------------------------------------------------   
    
    finalTickers = []
    for i in range(0,len(stocksFinal)):
        finalTickers.append(stocksFinal[i])
    for i in range(0,len(bondsFinal)):
        finalTickers.append(bondsFinal[i])
    for i in range(0,len(commFinal)):
        finalTickers.append(commFinal[i])
    for i in range(0,len(fundFinal)):
        finalTickers.append(fundFinal[i])
    
    finalWeights_short = []
    for key, val in stockWeights_short.items():
        x = FinalProfile[0]*stockWeights_short[key]  
        finalWeights_short.append(x)
    for key, val in bondWeights_short.items():
        x = FinalProfile[1]*bondWeights_short[key]
        finalWeights_short.append(x)
    for key, val in commWeights_short.items():
        x = FinalProfile[2]*commWeights_short[key]
        finalWeights_short.append(x)
    for key, val in fundWeights_short.items():
        x = FinalProfile[3]*fundWeights_short[key]
        finalWeights_short.append(x)

        
    endPort_short = {finalTickers[i]: finalWeights_short[i] for i in range(len(finalTickers))}
    
    shortData = price_tickers(finalTickers, start ='2019-01-01')
    
    print(endPort_short)
    print("\nPortfolio composition is: " + str(FinalProfile) + " (Stocks, Bonds, Currencies, Funds)")
    latest_prices = get_latest_prices(shortData)

    da_short = DiscreteAllocation(endPort_short, latest_prices, total_portfolio_value=alloAmount)
    allocation, leftover = da_short.lp_portfolio()
    print("Amount to invest: " + str(alloAmount))
    print("Discrete allocation:", allocation)
    print("Funds remaining: ${:.2f}".format(leftover))
    
    # Calculate expected returns and sample covariance
    shortMu = expected_returns.mean_historical_return(shortData)
    shortSig = risk_models.sample_cov(shortData)

    #Optimise each category
    shortEF = EfficientFrontier(shortMu, shortSig)
    shortEF.set_weights(endPort_short)
    shortPerformance = shortEF.portfolio_performance(verbose=True)
    print(shortPerformance)
    
    
     # Initialize some Monte Carlo paramters
    monte_carlo_runs = 2000
    days_to_simulate = 5
    loss_cutoff = 0.98 # count any losses larger than 5% (or -5%)

    # Call that simple function we wrote above
    what_we_got = shortData
    # Compute returns from those Adjusted Closes
    returns = what_we_got[finalTickers].pct_change()
        # This is basically what bt.get returned, just the returns
    # Remove the NA from returns; we always get 1 fewer returns than data
    returns = returns.dropna() # pretty easy command

    # Calculate mu and sigma
    mu = returns.mean() # mu was very easy using .mean method
    # sigma was harder, as I couldn't do it in one line
    #   the statistics package didn't know what to do without the loop
    #   So I copied the mu data structure and filled it in a loop
    sigma=mu.copy() # copy the mu series (a pandas datatype)
     # Loop over tickers and fill sigma up with the calculated standard deviation
    for i in finalTickers: # python loops over tickers no problem
        sigma[i]=stats.stdev(returns[i]) # fill up sigma with stdev's
            # There is probably a cleaner way to do that 

#----------------------------------------------------------------------------------
    # HISTORICAL VAR
#----------------------------------------------------------------------------------
    compound_returns = sigma.copy()
    total_simulations = 0
    bad_simulations = 0
    for run_counter in range(0,monte_carlo_runs): # Loop over runs    
        for i in finalTickers: # loop over tickers, below is done once per ticker
            # Loop over simulated days:
            compounded_temp = 1
            for simulated_day_counter in range(0,days_to_simulate): # loop over days
                simulated_return = choice(returns[i])
                compounded_temp = compounded_temp * (simulated_return + 1)        
            compound_returns[i]=compounded_temp # store compounded returns
        # Now see if those returns are bad by combining with weights
        portfolio_return = compound_returns.dot(finalWeights_short) # dot product
        if(portfolio_return<loss_cutoff):
            bad_simulations = bad_simulations + 1
        total_simulations = total_simulations + 1
    
    print("\nYour portfolio will lose",round((1-loss_cutoff)*100,3),"%",
          "over",days_to_simulate,"days", 
          bad_simulations/total_simulations, "of the time")
    
#----------------------------------------------------------------------------------   
    # PARAMETRIC VAR
#----------------------------------------------------------------------------------
    compound_returns = sigma.copy()
    total_simulations = 0
    bad_simulations = 0
    for run_counter in range(0,monte_carlo_runs): # Loop over runs    
        for i in finalTickers: # loop over tickers, below is done once per ticker
            # Loop over simulated days:
            compounded_temp = 1
            for simulated_day_counter in range(0,days_to_simulate): # loop over days
                simulated_return = np.random.normal(mu[i],sigma[i],1)
                compounded_temp = compounded_temp * (simulated_return + 1)
            compound_returns[i]=compounded_temp # store compounded returns
        # Now see if those returns are bad by combining with weights
        portfolio_return = compound_returns.dot(finalWeights_short) # dot product
        if(portfolio_return<loss_cutoff):
            bad_simulations = bad_simulations + 1
        total_simulations = total_simulations + 1
    
    print("Your portfolio will lose",round((1-loss_cutoff)*100,3),"%",
          "over",days_to_simulate,"days", 
          bad_simulations/total_simulations, "of the time")
    
    #fig= plt.figure()
    #fig.suptitle('Monte Carlo Simulation')
    #plt.plot(compound_returns)
    #plt.xlabel=('Day')
    #plt.ylable= ('Price')
   # plt.show()
    
    
    
### Medium Analysis
   
    print("\nPortfolio for 3 year analysis beginning 1/1/2017")
## Stocks Optimization
#-------------------------------------------------------------------------------
    #get data - returns
    stocksData_med = price_tickers(stocksFinal, startDate_med)

    # Calculate expected returns and sample covariance
    stocksMu_med = expected_returns.mean_historical_return(stocksData_med)
    stocksSig_med = risk_models.sample_cov(stocksData_med)

    #Optimise each category
    stocksEF_med = EfficientFrontier(stocksMu_med, stocksSig_med)
    stockWeights_med = stocksEF_med.max_sharpe(risk_free_rate=risk_free_rate)
  
## Commodity Optimization
#-------------------------------------------------------------------------------

    commData_med = price_tickers(commFinal, startDate_med)
    
    # Calculate expected returns and sample covariance
    commMu_med = expected_returns.mean_historical_return(commData_med)
    commSig_med = risk_models.sample_cov(commData_med)

    #Optimise each category
    commEF_med = EfficientFrontier(commMu_med, commSig_med)
    commWeights_med = commEF_med.max_sharpe(risk_free_rate=risk_free_rate)

## Bond Optimization
#-------------------------------------------------------------------------------
    
    bondsData_med = price_tickers(bondsFinal, startDate_med)
    
    # Calculate expected returns and sample covariance
    bondsMu_med = expected_returns.mean_historical_return(bondsData_med)
    bondsSig_med = risk_models.sample_cov(bondsData_med)
    
    #Optimise each category
    bondsEF_med = EfficientFrontier(bondsMu_med, bondsSig_med)
    bondWeights_med = bondsEF_med.max_sharpe(risk_free_rate=risk_free_rate)

## Fund Optimization    
#-------------------------------------------------------------------------------
    
    fundData_med = price_tickers(fundFinal, startDate_med)
    
    # Calculate expected returns and sample covariance
    fundMu_med = expected_returns.mean_historical_return(fundData_med)
    fundSig_med = risk_models.sample_cov(fundData_med)

    #Optimise each category
    fundEF_med = EfficientFrontier(fundMu_med, fundSig_med)
    fundWeights_med = fundEF_med.max_sharpe(risk_free_rate=risk_free_rate)
  
    
 ## Final Portfolio
#-------------------------------------------------------------------------------   
    
    finalTickers = []
    for i in range(0,len(stocksFinal)):
        finalTickers.append(stocksFinal[i])
    for i in range(0,len(bondsFinal)):
        finalTickers.append(bondsFinal[i])
    for i in range(0,len(commFinal)):
        finalTickers.append(commFinal[i])
    for i in range(0,len(fundFinal)):
        finalTickers.append(fundFinal[i])
    
    finalWeights_med = []
    for key, val in stockWeights_med.items():
        x = FinalProfile[0]*stockWeights_med[key]  
        finalWeights_med.append(x)
    for key, val in bondWeights_med.items():
        x = FinalProfile[1]*bondWeights_med[key]
        finalWeights_med.append(x)
    for key, val in commWeights_med.items():
        x = FinalProfile[2]*commWeights_med[key]
        finalWeights_med.append(x)
    for key, val in fundWeights_med.items():
        x = FinalProfile[3]*fundWeights_med[key]
        finalWeights_med.append(x)
        
    endPort_med = {finalTickers[i]: finalWeights_med[i] for i in range(len(finalTickers))}
    
    medData = price_tickers(finalTickers, start ='2017-01-01')
    
    print(endPort_med)
    print("\nPortfolio composition is: " + str(FinalProfile) + " (Stocks, Bonds, Currencies, Funds)")
    latest_prices = get_latest_prices(medData)

    da_med = DiscreteAllocation(endPort_med, latest_prices, total_portfolio_value=alloAmount)
    allocation, leftover = da_med.lp_portfolio()
    print("Amount to invest: " + str(alloAmount))
    print("Discrete allocation:", allocation)
    print("Funds remaining: ${:.2f}".format(leftover))
    
    # Calculate expected returns and sample covariance
    medMu = expected_returns.mean_historical_return(medData)
    medSig = risk_models.sample_cov(medData)

    #Optimise each category
    medEF = EfficientFrontier(medMu, medSig)
    medEF.set_weights(endPort_med)
    medPerformance = medEF.portfolio_performance(verbose=True)
    print(medPerformance)
    print(FinalProfile)
    
    # Call that simple function we wrote above
    what_we_got = medData
    # Compute returns from those Adjusted Closes
    returns = what_we_got[finalTickers].pct_change()
        # This is basically what bt.get returned, just the returns
    # Remove the NA from returns; we always get 1 fewer returns than data
    returns = returns.dropna() # pretty easy command

    # Calculate mu and sigma
    mu = returns.mean() # mu was very easy using .mean method
    # sigma was harder, as I couldn't do it in one line
    #   the statistics package didn't know what to do without the loop
    #   So I copied the mu data structure and filled it in a loop
    sigma=mu.copy() # copy the mu series (a pandas datatype)
     # Loop over tickers and fill sigma up with the calculated standard deviation
    for i in finalTickers: # python loops over tickers no problem
        sigma[i]=stats.stdev(returns[i]) # fill up sigma with stdev's
            # There is probably a cleaner way to do that 

#----------------------------------------------------------------------------------
    # HISTORICAL VAR
#----------------------------------------------------------------------------------
    compound_returns = sigma.copy()
    total_simulations = 0
    bad_simulations = 0
    for run_counter in range(0,monte_carlo_runs): # Loop over runs    
        for i in finalTickers: # loop over tickers, below is done once per ticker
            # Loop over simulated days:
            compounded_temp = 1
            for simulated_day_counter in range(0,days_to_simulate): # loop over days
                simulated_return = choice(returns[i])
                compounded_temp = compounded_temp * (simulated_return + 1)        
            compound_returns[i]=compounded_temp # store compounded returns
        # Now see if those returns are bad by combining with weights
        portfolio_return = compound_returns.dot(finalWeights_med) # dot product
        if(portfolio_return<loss_cutoff):
            bad_simulations = bad_simulations + 1
        total_simulations = total_simulations + 1
    
    print("\nYour portfolio will lose",round((1-loss_cutoff)*100,3),"%",
          "over",days_to_simulate,"days", 
          bad_simulations/total_simulations, "of the time")
    
#----------------------------------------------------------------------------------   
    # PARAMETRIC VAR
#----------------------------------------------------------------------------------
    compound_returns = sigma.copy()
    total_simulations = 0
    bad_simulations = 0
    for run_counter in range(0,monte_carlo_runs): # Loop over runs    
        for i in finalTickers: # loop over tickers, below is done once per ticker
            # Loop over simulated days:
            compounded_temp = 1
            for simulated_day_counter in range(0,days_to_simulate): # loop over days
                simulated_return = np.random.normal(mu[i],sigma[i],1)
                compounded_temp = compounded_temp * (simulated_return + 1)
            compound_returns[i]=compounded_temp # store compounded returns
        # Now see if those returns are bad by combining with weights
        portfolio_return = compound_returns.dot(finalWeights_med) # dot product
        if(portfolio_return<loss_cutoff):
            bad_simulations = bad_simulations + 1
        total_simulations = total_simulations + 1
    
    print("Your portfolio will lose",round((1-loss_cutoff)*100,3),"%",
          "over",days_to_simulate,"days", 
          bad_simulations/total_simulations, "of the time")
    
    #fig= plt.figure()
    #fig.suptitle('Monte Carlo Simulation')
    #plt.plot(compound_returns)
    #plt.xlabel=('Day')
    #plt.ylable= ('Price')
    #plt.show()
    
    
### Long Analysis
    
    print("\nPortfolio for 5 year analysis beginning 1/1/2015")
## Stocks Optimization
#-------------------------------------------------------------------------------
    #get data - returns
    stocksData_long = price_tickers(stocksFinal, startDate_long)

    # Calculate expected returns and sample covariance
    stocksMu_long = expected_returns.mean_historical_return(stocksData_long)
    stocksSig_long = risk_models.sample_cov(stocksData_long)

    #Optimise each category
    stocksEF_long = EfficientFrontier(stocksMu_long, stocksSig_long)
    stockWeights_long = stocksEF_long.max_sharpe(risk_free_rate=risk_free_rate)
  
## Commodity Optimization
#-------------------------------------------------------------------------------

    commData_long = price_tickers(commFinal, startDate_long)
    
    # Calculate expected returns and sample covariance
    commMu_long = expected_returns.mean_historical_return(commData_long)
    commSig_long = risk_models.sample_cov(commData_long)

    #Optimise each category
    commEF_long = EfficientFrontier(commMu_long, commSig_long)
    commWeights_long = commEF_long.max_sharpe(risk_free_rate=risk_free_rate)

## Bond Optimization
#-------------------------------------------------------------------------------
    
    bondsData_long = price_tickers(bondsFinal, startDate_long)
    
    # Calculate expected returns and sample covariance
    bondsMu_long = expected_returns.mean_historical_return(bondsData_long)
    bondsSig_long = risk_models.sample_cov(bondsData_long)
    
    #Optimise each category
    bondsEF_long = EfficientFrontier(bondsMu_long, bondsSig_long)
    bondWeights_long = bondsEF_long.max_sharpe(risk_free_rate=risk_free_rate)

## Fund Optimization    
#-------------------------------------------------------------------------------
    
    fundData_long = price_tickers(fundFinal, startDate_long)
    
    # Calculate expected returns and sample covariance
    fundMu_long = expected_returns.mean_historical_return(fundData_long)
    fundSig_long = risk_models.sample_cov(fundData_long)

    #Optimise each category
    fundEF_long = EfficientFrontier(fundMu_long, fundSig_long)
    fundWeights_long = fundEF_long.max_sharpe(risk_free_rate=risk_free_rate)
  
    
 ## Final Portfolio
#-------------------------------------------------------------------------------   
    
    finalTickers = []
    for i in range(0,len(stocksFinal)):
        finalTickers.append(stocksFinal[i])
    for i in range(0,len(bondsFinal)):
        finalTickers.append(bondsFinal[i])
    for i in range(0,len(commFinal)):
        finalTickers.append(commFinal[i])
    for i in range(0,len(fundFinal)):
        finalTickers.append(fundFinal[i])
    
    finalWeights_long = []
    for key, val in stockWeights_long.items():
        x = FinalProfile[0]*stockWeights_long[key]  
        finalWeights_long.append(x)
    for key, val in bondWeights_long.items():
        x = FinalProfile[1]*bondWeights_long[key]
        finalWeights_long.append(x)
    for key, val in commWeights_long.items():
        x = FinalProfile[2]*commWeights_long[key]
        finalWeights_long.append(x)
    for key, val in fundWeights_long.items():
        x = FinalProfile[3]*fundWeights_long[key]
        finalWeights_long.append(x)
        
    endPort_long = {finalTickers[i]: finalWeights_long[i] for i in range(len(finalTickers))}
    
    longData = price_tickers(finalTickers, start ='2015-01-01')
    
    print(endPort_long)
    print("\nPortfolio composition is: " + str(FinalProfile) + " (Stocks, Bonds, Currencies, Funds)")
    latest_prices = get_latest_prices(longData)

    da_long = DiscreteAllocation(endPort_long, latest_prices, total_portfolio_value=alloAmount)
    allocation, leftover = da_long.lp_portfolio()
    print("Amount to invest: " + str(alloAmount))
    print("Discrete allocation:", allocation)
    print("Funds remaining: ${:.2f}".format(leftover))
    
    # Calculate expected returns and sample covariance
    longMu = expected_returns.mean_historical_return(longData)
    longSig = risk_models.sample_cov(longData)

    #Optimise each category
    longEF = EfficientFrontier(longMu, longSig)
    longEF.set_weights(endPort_long)
    longPerformance = longEF.portfolio_performance(verbose=True)
    print(longPerformance)
    print(FinalProfile)
    
    # Call that simple function we wrote above
    what_we_got = longData
    # Compute returns from those Adjusted Closes
    returns = what_we_got[finalTickers].pct_change()
        # This is basically what bt.get returned, just the returns
    # Remove the NA from returns; we always get 1 fewer returns than data
    returns = returns.dropna() # pretty easy command

    # Calculate mu and sigma
    mu = returns.mean() # mu was very easy using .mean method
    # sigma was harder, as I couldn't do it in one line
    #   the statistics package didn't know what to do without the loop
    #   So I copied the mu data structure and filled it in a loop
    sigma=mu.copy() # copy the mu series (a pandas datatype)
     # Loop over tickers and fill sigma up with the calculated standard deviation
    for i in finalTickers: # python loops over tickers no problem
        sigma[i]=stats.stdev(returns[i]) # fill up sigma with stdev's
            # There is probably a cleaner way to do that 

#----------------------------------------------------------------------------------
    # HISTORICAL VAR
#----------------------------------------------------------------------------------
    compound_returns = sigma.copy()
    total_simulations = 0
    bad_simulations = 0
    for run_counter in range(0,monte_carlo_runs): # Loop over runs    
        for i in finalTickers: # loop over tickers, below is done once per ticker
            # Loop over simulated days:
            compounded_temp = 1
            for simulated_day_counter in range(0,days_to_simulate): # loop over days
                simulated_return = choice(returns[i])
                compounded_temp = compounded_temp * (simulated_return + 1)        
            compound_returns[i]=compounded_temp # store compounded returns
        # Now see if those returns are bad by combining with weights
        portfolio_return = compound_returns.dot(finalWeights_long) # dot product
        if(portfolio_return<loss_cutoff):
            bad_simulations = bad_simulations + 1
        total_simulations = total_simulations + 1
    
    print("\nYour portfolio will lose",round((1-loss_cutoff)*100,3),"%",
          "over",days_to_simulate,"days", 
          bad_simulations/total_simulations, "of the time")
    
#----------------------------------------------------------------------------------   
    # PARAMETRIC VAR
#----------------------------------------------------------------------------------
    compound_returns = sigma.copy()
    total_simulations = 0
    bad_simulations = 0
    for run_counter in range(0,monte_carlo_runs): # Loop over runs    
        for i in finalTickers: # loop over tickers, below is done once per ticker
            # Loop over simulated days:
            compounded_temp = 1
            for simulated_day_counter in range(0,days_to_simulate): # loop over days
                simulated_return = np.random.normal(mu[i],sigma[i],1)
                compounded_temp = compounded_temp * (simulated_return + 1)
            compound_returns[i]=compounded_temp # store compounded returns
        # Now see if those returns are bad by combining with weights
        portfolio_return = compound_returns.dot(finalWeights_long) # dot product
        if(portfolio_return<loss_cutoff):
            bad_simulations = bad_simulations + 1
        total_simulations = total_simulations + 1
    
    print("Your portfolio will lose",round((1-loss_cutoff)*100,3),"%",
          "over",days_to_simulate,"days", 
          bad_simulations/total_simulations, "of the time")
    
    #fig= plt.figure()
    #fig.suptitle('Monte Carlo Simulation')
    #plt.plot(compound_returns)
    #plt.xlabel=('Day')
    #plt.ylable= ('Price')
    #plt.show()
# set up button to calculate results of the assessment
calc = tk.Button(root, text="calculate", command=CalculateProfile)
calc.grid(row=30, column=1, pady = 5, sticky=tk.NE )


root.mainloop()
