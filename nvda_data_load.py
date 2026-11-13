import yfinance as yf
import pandas as pd 

#Download historical data for a specific stock 
ticker = "NVDA" 
df = yf.download(ticker, start="2016-01-01", end="2026-11-12")


#Quick look at the data 
print(df.head())
print (df.tail())
print (df.shape)
print (df.info())

#Save the data to a CSV file
df.to_csv("nvda_data.csv")