from pandas_datareader import data as pdr
import pandas as pd
import yfinance as yf
yf.pdr_override()
start = '2000-01-04'
dow = pdr.get_data_yahoo('^DJI',start)
kospi = pdr.get_data_yahoo('^KS11',start)

import matplotlib.pyplot as plt
#plt.figure(figsize=(9,5))
#plt.plot(dow.index,dow.Close,'r--',label='Dow Jones Industrial')
#plt.plot(kospi.index,kospi.Close,'b',label='KOSPI')
#plt.grid(True)
#plt.legend(loc='best')
#plt.show()

d = (dow.Close / dow.Close.loc[start]) * 100
k = (kospi.Close / kospi.Close.loc[start]) * 100
"""
plt.figure(figsize=(9,5))
plt.plot(dow.index,d,'r--',label='Dow Jones Industrial')
plt.plot(kospi.index,k,'b',label='KOSPI')
plt.grid(True)
plt.legend(loc='best')
plt.show()
"""
print(len(dow),len(kospi))
df = pd.DataFrame({'DOW':dow['Close'],'KOSPI':kospi['Close']})
print(df)
df = df.fillna(method='bfill')
df = df.fillna(method='ffill')
plt.figure(figsize=(7,7))
plt.scatter(df['DOW'],df['KOSPI'],marker='.')
plt.show()
