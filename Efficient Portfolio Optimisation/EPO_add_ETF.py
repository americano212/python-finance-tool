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
def get_stock_code():
    Stock_Info_txt = open('stock_code.txt','r')
    while True:
        line = Stock_Info_txt.readline()
        if not line:
            break
        line_split = line.split(',')
        line_split[-1] = line_split[-1][:-1]
        Stock_Code.append(line_split[0])
        Stock_Name.append(line_split[1])

def get_dcf_data():
    Stock_DCF_txt = open('dcf_result.txt','r')
    while True:
        line = Stock_DCF_txt.readline()
        if not line:
            break
        line = line [:-1]
        DCF_Result.append(int(line))
def Get_Stock_Data_Except(Code: str,start_ymd: str) -> None:
    if (Code=="E364980"):
        kind = [['096770',26.21],['051910',25.34],['006400',23.11],['003670',7.76],['011790',5.01],['020150',2.63]]
        tmp = []
        tmp_close = []
        for i in range(len(kind)):
            get_pdr = pdr.get_data_yahoo('{0}.KS'.format(kind[i][0]),start=start_ymd,end=end_ymd)
            tmp.append((get_pdr['Close']/get_pdr['Close']['2020-01-02'])*100)
        close_matrix = np.matrix(pd.DataFrame(tmp))
        rate = []
        for i in range(len(kind)):
            rate.append(kind[i][1])
        rate_matrix = np.matrix(rate)
        result = pd.DataFrame((rate_matrix@close_matrix).T)
        result.index = pd.DataFrame(tmp).columns
        Stock_Data_Close.append(result)
        get_pdr = pdr.get_data_yahoo('{0}.KS'.format(Code[1:]),start='2021-05-01')
        Stock_Data_Close_Today.append(get_pdr['Close'][-1])
    if (Code=="E377990"):
        kind = [['010060',17.8],['112610',11.67],['009830',11.24],['006260',9.75],['336260',8.24],['011930',4.05]]
        tmp = []
        tmp_close = []
        for i in range(len(kind)):
            get_pdr = pdr.get_data_yahoo('{0}.KS'.format(kind[i][0]),start=start_ymd,end=end_ymd)
            tmp.append((get_pdr['Close']/get_pdr['Close']['2020-01-02'])*100)
        close_matrix = np.matrix(pd.DataFrame(tmp))
        rate = []
        for i in range(len(kind)):
            rate.append(kind[i][1])
        rate_matrix = np.matrix(rate)
        result = pd.DataFrame((rate_matrix@close_matrix).T)
        result.index = pd.DataFrame(tmp).columns
        Stock_Data_Close.append(result)
        get_pdr = pdr.get_data_yahoo('{0}.KS'.format(Code[1:]),start='2021-05-01')
        Stock_Data_Close_Today.append(get_pdr['Close'][-1])

def Get_Stock_Data(Code: str,start_ymd: str) -> None:
    if (Code[0]=='E'):
        Get_Stock_Data_Except(Code,start_ymd)
    else:
        get_pdr = pdr.get_data_yahoo('{0}.KS'.format(Code),start=start_ymd,end=end_ymd)
        Stock_Data_Close.append(get_pdr['Close'])
        get_pdr = pdr.get_data_yahoo('{0}.KS'.format(Code),start='2021-05-01')
        Stock_Data_Close_Today.append(get_pdr['Close'][-1])

def Get_Stock_Change(One_Stock_Data_Close):
    Change = (One_Stock_Data_Close / One_Stock_Data_Close.shift(1) - 1)*100
    Change.iloc[0]=0
    Change_list.append(Change)

def BackTesting():
    pass

def main():
    get_stock_code()
    get_dcf_data()
    for info in Stock_Code:
        Get_Stock_Data(info,start_ymd)
    for data in Stock_Data_Close:
        Get_Stock_Change(data)

    expected_profit = []
    for idx in range(len(Stock_Code)):
        expected_profit.append((DCF_Result[idx]-Stock_Data_Close_Today[idx])/Stock_Data_Close_Today[idx])
    Change_df = pd.concat(Change_list,axis=1)
    Change_df.columns = Stock_Name

    Change_avg = Change_df.mean()
    print(Change_df)
    Change_df = Change_df+0.00001*np.random.rand(Change_df.shape[0],Change_df.shape[1])
    Change_cov = Change_df.cov()
    print(Change_cov)
    Change_cov_inv = pd.DataFrame(np.matrix(Change_cov).I,Change_cov.columns,Change_cov.index)
    #Change_cov_inv = pd.DataFrame(np.mat(np.array(Change_cov)).I)
    ones = np.ones(Change_cov_inv.shape[1])

    weight = (Change_cov@ones)/(ones.T@Change_cov@ones)
    print("="*50)
    print("Minimum Variance Portfolio")
    print(weight*100)
    #print(weight.T@Change_cov@weight)


    weight=(Change_cov@Change_avg)/(ones.T@Change_cov_inv@Change_avg)
    print("="*50)
    print("Tangent (Max Sharp ratio) Portfolio")
    print(weight*100/weight.sum())
    print("="*50)

    weight_fix = weight*100/weight.sum()
    profit = 0
    for idx in range(len(Stock_Code)):
        profit+=expected_profit[idx]*weight_fix[idx]
    print("기대 수익률 : {0}%".format(round(profit,2)))

    print(Change_df.corr())
if __name__ == '__main__':
    main()
