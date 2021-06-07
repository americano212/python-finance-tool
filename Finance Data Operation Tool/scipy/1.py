from pandas_datareader import data as pdr
import pandas as pd
import yfinance as yf
from scipy import stats
import matplotlib.pyplot as plt
yf.pdr_override()
start = '2000-01-04'
dow = pdr.get_data_yahoo('^DJI',start)
kospi = pdr.get_data_yahoo('^KS11',start)
d = (dow.Close / dow.Close.loc[start]) * 100
k = (kospi.Close / kospi.Close.loc[start]) * 100
df = pd.DataFrame({'X':dow['Close'],'Y':kospi['Close']})
df = df.fillna(method='bfill')
df = df.fillna(method='ffill')
model = stats.linregress(df['X'],df['Y'])
print(model)
print(df.corr())
r_value = df['X'].corr(df['Y'])
r_squared = r_value**2
print(r_squared)
regr = stats.linregress(df.X,df.Y)
regr_line = f'Y = {regr.slope:.2f} * X + {regr.intercept:.2f}'
plt.figure(figsize=(7,7))
plt.plot(df.X,df.Y,'.')
plt.plot(df.X,regr.slope * df.X + regr.intercept, 'r')
plt.legend(['DOW x KOSPI',regr_line])
plt.show()
