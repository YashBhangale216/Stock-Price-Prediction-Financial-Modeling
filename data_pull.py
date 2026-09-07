# import yfinance as yf
# import pandas as pd 

# #Download historical data for a specific stock 
# ticker = "NVDA" 
# df = yf.download(ticker, start="2016-01-01", end="2026-08-13")


# #Quick look at the data 
# print(df.head())
# print (df.tail())
# print (df.shape)
# print (df.info())

# #Save the data to a CSV file
# df.to_csv("nvda_data.csv")





#importing libraries
import yfinance as yf
import pandas as pd


# Download historical data for a specific stock
ticker = "NVDA"
df = yf.download(ticker, start="2016-01-01", end="2026-08-16", auto_adjust=True)

# clean up messy column names
if isinstance (df.columns,  pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

# Reset index so date becomes a normal column
df.reset_index(inplace=True)


print("Shape:", df.shape)
print(df.head)
print(df.tail)
print(df.isnull().sum())


#save the file into CSV 
df.to_csv("nvda_data.csv", index=False)