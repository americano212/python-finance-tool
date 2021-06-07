from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()

sec = pdr.get_data_yahoo('005930.KS',start='2018-05-04')
sec_dpc = (sec['Close'] / sec['Close'].shift(1) - 1)*100
sec_dpc.iloc[0]=0
sec_dpc_cs = sec_dpc.cumsum() #누적합

msft = pdr.get_data_yahoo('MSFT',start='2018-05-04')
msft_dpc = (msft['Close'] / msft['Close'].shift(1) - 1)*100
msft_dpc.iloc[0]=0
msft_dpc_cs = msft_dpc.cumsum()

import matplotlib.pyplot as plt
plt.plot(sec.index,sec_dpc_cs,'b',label='Samsung Electronics')
plt.plot(msft.index,msft_dpc_cs,'r--',label='ms')
plt.grid(True)
plt.show()
