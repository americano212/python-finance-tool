from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override() #빠르게 data 다운로드

sec = pdr.get_data_yahoo('005930.KS',start='2018-05-04')
msft = pdr.get_data_yahoo('MSFT',start='2018-05-04')
print(sec.head(10))
tmp_msft = msft.drop(columns='Volume')

#import matplotlib.pyplot as plt
#plt.plot(sec.index,sec.Close,'b',label='Samsung Electronics')
#plt.plot(msft.index,msft.Close,'r--',label='Microsoft')
#plt.legend(loc='best')
#plt.show()
print(sec['Close'])
print(sec['Close'].shift(1))
sec_dpc = (sec['Close'] / sec['Close'].shift(1) - 1)*100
print(sec_dpc.head())
sec_dpc.iloc[0]=0
print(sec_dpc.head())

import matplotlib.pyplot as plt
plt.hist(sec_dpc,bins=18) #변동률을 18개의 구간으로 나누어 빈도수를 표시한
plt.grid(True)
#plt.show()
print(sec_dpc.describe())
sec_dpc_cs = sec_dpc.cumsum()
print(sec_dpc_cs)
