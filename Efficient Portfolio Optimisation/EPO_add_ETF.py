from pandas_datareader import data as pdr
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np
from pykiwoom.kiwoom import *
yf.pdr_override()
from statsmodels import regression
import statsmodels.api as sm
import seaborn as sns
from statsmodels.formula.api import ols

Stock_Code = []
Stock_Data_Close = []
Stock_Data_Close_Today = []
Stock_Name = []
start_ymd = '2020-01-01'
end_ymd = '2021-01-01'
end=check_ymd = '2021-05-21'
Change_list = []
DCF_Result = []
expected_profit = []
BackTesting_Data_Close = []
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

def Get_Stock_Data(Code: str,start_ymd: str,flag=0) -> None:
    if (Code[0]=='E'):
        if (flag):
            get_pdr = pdr.get_data_yahoo('{0}.KS'.format(Code[1:]),start=start_ymd)
            BackTesting_Data_Close.append(get_pdr['Close'])
        else:
            Get_Stock_Data_Except(Code,start_ymd)
    else:
        if (flag):
            get_pdr = pdr.get_data_yahoo('{0}.KS'.format(Code),start=start_ymd)
            BackTesting_Data_Close.append(get_pdr['Close'])
        else:

            get_pdr = pdr.get_data_yahoo('{0}.KS'.format(Code),start=start_ymd,end=end_ymd)
            Stock_Data_Close.append(get_pdr['Close'])
            get_pdr = pdr.get_data_yahoo('{0}.KS'.format(Code),start='2021-05-01',end=check_ymd)
            Stock_Data_Close_Today.append(get_pdr['Close'][-1])

def Get_Stock_Change(One_Stock_Data_Close):
    Change = (One_Stock_Data_Close / One_Stock_Data_Close.shift(1) - 1)*100
    Change.iloc[0]=0
    Change_list.append(Change)

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

def Make_MaxSharpeRatio_PF():
    #1년간의 수익률 변화를 담고 있는 DataFrame
    Change_df = pd.concat(Change_list,axis=1)
    Change_df.columns = Stock_Name
    Change_avg = Change_df.mean()
    #상관관계가 같은 경우  Covariance matrix과 inv를 만들기 위해 노이즈 추가(실제 값엔 영향없음)
    Change_df = Change_df+0.00001*np.random.rand(Change_df.shape[0],Change_df.shape[1])
    #Covariance matrix와 그의 Inverse matrix
    Change_cov = Change_df.cov()
    f = plt.figure(figsize=(19, 15))
    plt.matshow(Change_cov, fignum=f.number)
    plt.xticks(range(Change_df.select_dtypes(['number']).shape[1]), Change_df.select_dtypes(['number']).columns, fontsize=14, rotation=45)
    plt.yticks(range(Change_df.select_dtypes(['number']).shape[1]), Change_df.select_dtypes(['number']).columns, fontsize=14)
    cb = plt.colorbar()
    cb.ax.tick_params(labelsize=14)
    plt.title('Covariance Matrix', fontsize=16);
    plt.show()

    Change_cov_inv = pd.DataFrame(np.matrix(Change_cov).I,Change_cov.columns,Change_cov.index)
    # 1로 구성된 행렬 생성
    ones = np.ones(Change_cov_inv.shape[1])
    #Portfolio 내 자산 비중 행렬 weight 계산
    weight=(Change_cov@Change_avg)/(ones.T@Change_cov_inv@Change_avg)
    #이하 출력
    print("="*50)
    print("Tangent (Max Sharp ratio) Portfolio")
    print(weight*100/weight.sum())

    global weight_save
    weight_save = weight*100/weight.sum()
    print("="*50)

    weight_fix = weight*100/weight.sum()
    profit = 0
    for idx in range(len(Stock_Code)):
        profit+=expected_profit[idx]*weight_fix[idx]
    print("기대 수익률 : {0}%".format(round(profit,2)))
    print(Change_df.corr())
    f = plt.figure(figsize=(19, 15))
    plt.matshow(Change_df.corr(), fignum=f.number)
    plt.xticks(range(Change_df.select_dtypes(['number']).shape[1]), Change_df.select_dtypes(['number']).columns, fontsize=14, rotation=45)
    plt.yticks(range(Change_df.select_dtypes(['number']).shape[1]), Change_df.select_dtypes(['number']).columns, fontsize=14)
    cb = plt.colorbar()
    cb.ax.tick_params(labelsize=14)
    plt.title('Correlation Matrix', fontsize=16);
    plt.show()


def make_pie_chart():
    ratio = list(np.array(weight_save))
    labels = list(weight_save.index)
    explode = [0.2 for _ in range(len(ratio))]
    print(ratio)
    print(labels)
    plt.pie(ratio, labels=labels, autopct='%.1f%%', explode=explode, shadow=True)
    plt.show()

def Compare_Market():
    ratio = np.array(weight_save)[:-2]
    for info in Stock_Code:
        if (info[0]!='E'):
            Get_Stock_Data(info,'2021-01-01',flag=1)
    S = []
    K = []
    data_fix = []
    for data in BackTesting_Data_Close:
        data_fix.append(((data.pct_change(1)+1).cumprod()).fillna(1))
        S.append(data.pct_change())
    S = ((ratio@np.matrix(pd.DataFrame(S)))).tolist()[0]

    data_fix_2 = (ratio@np.matrix(pd.DataFrame(data_fix)-1)).tolist()[0]
    get_pdr = pdr.get_data_yahoo('069500.KS',start='2021-01-01')
    kdx = list(get_pdr['Close'])
    K = get_pdr['Close'].pct_change()
    idx = get_pdr.index
    SWIC_ETF = []
    KODEX_ETF = []
    for data in data_fix_2:
        SWIC_ETF.append(data)
    for data in kdx:
        KODEX_ETF.append(data*100/kdx[0]-100)
    SWIC_ETF = pd.Series(SWIC_ETF)
    SWIC_ETF.index = idx
    KODEX_ETF = pd.Series(KODEX_ETF)
    KODEX_ETF.index = idx
    plt.plot(SWIC_ETF,'b',label='ESG_Active_Fund')
    plt.plot(KODEX_ETF,'r--',label='KODEX 200')
    plt.ylabel('Change')
    #ax.set_yticklabels([])
    plt.grid(True)
    plt.legend(loc='best')
    plt.show()
    S = pd.Series(S)
    print(S)
    print("Sharpe Ratio는 {0}".format(SWIC_ETF.mean()/SWIC_ETF.std()))
    print("Sharpe Ratio는 {0}".format(S.mean()/S.std()))
    print(S,K)


    S.index = idx
    K=K*100
    df = pd.concat([S,K],axis=1)
    df.columns = ['ESG_Active_Fund','KODEX']
    df = df.dropna()
    print(df.head())
    with plt.style.context('seaborn'):
        sns.jointplot('ESG_Active_Fund','KODEX',data=df,kind='reg')
    plt.show()
    daily_ols = ols('ESG_Active_Fund~1+KODEX',data=df).fit()
    print(daily_ols.summary())
    print(SWIC_ETF.mean()/0.7838)
    print(S.mean()/0.7838)
def Login_kiwoom():
    kiwoom = Kiwoom()
    kiwoom.CommConnect(block=True)

def Buy_kiwoom(Code,count):
    stock_account = kiwoom.GetLoginInfo("ACCNO")[0]
    # Code, count, 시장가주문 매수
    kiwoom.SendOrder("시장가매수", "0101", stock_account, 1, Code, count, 0, "03", "")

def main():
    get_stock_code()
    get_dcf_data()
    for info in Stock_Code:
        Get_Stock_Data(info,start_ymd)
    for data in Stock_Data_Close:
        Get_Stock_Change(data)


    for idx in range(len(Stock_Code)):
        expected_profit.append((DCF_Result[idx]-Stock_Data_Close_Today[idx])/Stock_Data_Close_Today[idx])

    Make_MaxSharpeRatio_PF()
    #make_pie_chart()

    Compare_Market()

if __name__ == '__main__':
    main()
