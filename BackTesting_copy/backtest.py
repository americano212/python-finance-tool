from pandas_datareader import data as pdr
import pandas as pd
import matplotlib.pyplot as plt

import yfinance as yf
yf.pdr_override()

# init global value
Stock_Code = [] #Ex) [[stock_code,full_name,short_name], ...]
Stock_Data = []
Stock_Data_Close = []
Stock_Data_Close_Today = []
DCF_Result = []
BT_Result_ALL = []
start_ymd = '2017-01-01'
start_money = 10**8
Cutline_Percent = 10
BackTesting_Term = 250
Can_Sell = False
Sell_Percent = 10000
Ratio = []

def Get_Stock_Data(Code: str,start_ymd: str) -> None:
    print("종목 코드 : {0}의 주가 데이터 가져오는 중(시작 : {1})".format(Code,start_ymd))
    get_pdr = pdr.get_data_yahoo('{0}.KS'.format(Code),start=start_ymd)
    Stock_Data.append(get_pdr)
    Stock_Data_Close.append(get_pdr['Close'])
    Stock_Data_Close_Today.append(get_pdr['Close'][-1])

def Portfolio_Include(Stock_Data_Close_Today: list, Stock_Code: list, DCF_Result:list, Cutline_Percent: int) -> list:
    result = []
    print('='*80)
    for i in range(len(Stock_Code)):
        Possible_Rising = (DCF_Result[i] / Stock_Data_Close_Today[i])*100
        if (Possible_Rising > Cutline_Percent+100):
            result.append([Stock_Code[i][0],1])
            print('종목 코드 : {0}의 상승 가능성은 {1:2.2f}% 입니다. 포트폴리오에 추가합니다.'.format(Stock_Code[i][0],Possible_Rising-100))
        else:
            result.append([Stock_Code[i][0],0])
            print('종목 코드 : {0}의 상승 가능성은 {1:2.2f}% 입니다. 포트폴리오에 추가하지 않습니다.'.format(Stock_Code[i][0],Possible_Rising-100))
    print('='*80)
    return result

def BackTesting(One_Stock_Data_Close, BackTesting_Term: int,Can_Sell: bool,Sell_Percent: int) -> pd.Series:
    result = pd.Series([])
    Change = (One_Stock_Data_Close / One_Stock_Data_Close.shift(1) - 1)*100
    Change.iloc[0]=0
    Change_cs = Change.cumsum()
    #print(Change_cs)
    for i in range(len(Change_cs)-BackTesting_Term-1):
        Delta = sum([Change_cs[BackTesting_Term+i-1],Change_cs[BackTesting_Term+i],Change_cs[BackTesting_Term+i+1]])/3 - Change_cs[i]
        result[str(Change_cs.index[i])[:-9]] = Delta
    #print(result.describe())
    return result

def Make_BT_Graph(BT_Result_ALL):
    for BT_result in BT_Result_ALL:
        plt.scatter(BT_result.index,BT_result,s=1, label = 'line graph')
        plt.plot(BT_result.index,BT_result, alpha = 0.5)
        plt.grid()
        ax = plt.axes()
        ax.set_xticks([])
    plt.show()

def Portfolio_Result(Ratio: list,start_money: int):
    pass


def Make_Ratio(Portfolio_Stock: list):
    Ratio = [0 for _ in range(len(Portfolio_Stock))]
    

def main():
    Stock_Info_txt = open('stock_code.txt','r')
    Stock_DCF_txt = open('dcf_result.txt','r')

    while True:
        line = Stock_Info_txt.readline()
        if not line:
            break
        #print(line,end='')
        line_split = line.split(',')
        line_split[-1] = line_split[-1][:-1]
        Stock_Code.append(line_split)
    #print(Stock_Code)

    while True:
        line = Stock_DCF_txt.readline()
        if not line:
            break
        line = line [:-1]
        DCF_Result.append(int(line))
    print('='*80)
    for Code in Stock_Code:
        Get_Stock_Data(Code[0],start_ymd)
    print('='*80)

    # Data Except clear
    for i in range(len(Stock_Data_Close[5])):
        if Stock_Data_Close[5][i] > 1000000:
            Stock_Data_Close[5].iloc[i]=Stock_Data_Close[5][i]/100

    Portfolio_Stock = Portfolio_Include(Stock_Data_Close_Today, Stock_Code, DCF_Result, Cutline_Percent)
    print(Portfolio_Stock)
    for i in range(len(Stock_Code)):
        print('='*80)
        print('종목코드 : {0}의 백테스팅 시작'.format(Stock_Code[i][0]))
        BT_result = BackTesting(Stock_Data_Close[i], BackTesting_Term,Can_Sell,Sell_Percent)
        BT_Result_ALL.append(BT_result)

    #Make_BT_Graph(BT_Result_ALL)

    Stock_Info_txt.close()

if __name__ == '__main__':
    main()
