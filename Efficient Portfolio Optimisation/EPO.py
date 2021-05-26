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

def Get_Stock_Data(Code: str,start_ymd: str) -> None:
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
def Make_min_var_PF():
    Change_df = pd.concat(Change_list,axis=1)
    Change_df.columns = Stock_Name
    Change_avg = Change_df.mean()
    Change_df = Change_df+0.00001*np.random.rand(Change_df.shape[0],Change_df.shape[1])
    Change_cov = Change_df.cov()
    Change_cov_inv = pd.DataFrame(np.matrix(Change_cov).I,Change_cov.columns,Change_cov.index)
    ones = np.ones(Change_cov_inv.shape[1])
    weight = (Change_cov@ones)/(ones.T@Change_cov@ones)
    print("="*50)
    print("Minimum Variance Portfolio")
    print(weight*100)
    #print(weight.T@Change_cov@weight)

def Make_max_sr_PF():
    Change_df = pd.concat(Change_list,axis=1)
    Change_df.columns = Stock_Name
    Change_avg = Change_df.mean()
    Change_df = Change_df+0.00001*np.random.rand(Change_df.shape[0],Change_df.shape[1])
    Change_cov = Change_df.cov()
    Change_cov_inv = pd.DataFrame(np.matrix(Change_cov).I,Change_cov.columns,Change_cov.index)
    ones = np.ones(Change_cov_inv.shape[1])
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


    Make_max_sr_PF()

    print(Change_df.corr())
if __name__ == '__main__':
    main()
