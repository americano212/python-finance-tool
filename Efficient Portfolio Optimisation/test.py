from pandas_datareader import data as pdr
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np
yf.pdr_override()
Stock_Code = []
Stock_Data_Close = []
Stock_Data_Close_Today = []
Stock_Name = []
start_ymd = '2020-01-01'
end_ymd = '2021-01-01'
Change_list = []
DCF_Result = []

def Get_Stock_Data_Except(Code: str,start_ymd: str) -> None:
    if (Code=="E364980"):
        kind = [['096770',26.21],['051910',25.34],['006400',23.11],['003670',7.76],['011790',5.01],['020150',2.63]]
        tmp = []
        tmp_close = []
        for i in range(len(kind)):
            get_pdr = pdr.get_data_yahoo('{0}.KS'.format(kind[i][0]),start=start_ymd,end=end_ymd)
            tmp.append((get_pdr['Close']/get_pdr['Close']['2020-01-02'])*100)
        print(pd.DataFrame(tmp))
        print(pd.DataFrame(tmp).columns)
        print(np.matrix(pd.DataFrame(tmp)))
        close_matrix = np.matrix(pd.DataFrame(tmp))
        rate = []
        for i in range(len(kind)):
            rate.append(kind[i][1])
        rate_matrix = np.matrix(rate)
        print(rate_matrix@close_matrix)
        result = pd.DataFrame((rate_matrix@close_matrix).T)
        result.index = pd.DataFrame(tmp).columns
        print(result.sum())
Get_Stock_Data_Except("E364980",'2020-01-01')
