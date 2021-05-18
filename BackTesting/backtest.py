from pandas_datareader import data as pdr # pandas를 이용해서 야후 파이낸스
import pandas as pd # 2차원 데이터 다루는 툴
import matplotlib.pyplot as plt # 그래프 그리는 툴

import yfinance as yf #야후 파이낸스에서 데이터 제공
yf.pdr_override()

# init global value
Stock_Code = [] #Ex) [[stock_code,full_name,short_name], ...]
Stock_Data = [] # 기간동안 저가, 고가,종가, 거래량 등 전체 정보
Stock_Data_Close = [] # 기간동안 종가를 저장
Stock_Data_Close_Today = [] # 오늘의 종가를 저장 [int,int,int,int,...]
DCF_Result = [] # DCF 결과 저장
BT_Result_ALL = [] # 백테스팅 결과 전체 [[일자,1년 수익률],...]
start_ymd = '2017-01-01' # 백테스팅 시작일
start_money = 10**8 # 시작 금액
Cutline_Percent = 10 # DCF 결과가 현재 주가에 비해서 얼마나 높은걸 포트폴리오에 넣을지
BackTesting_Term = 250 #백테스팅 기한
Can_Sell = False #중간에 파는걸 구현할지 그냥 기간 종가만 볼지
Sell_Percent = 10000 #나중에 백테스팅 계량할때 쓸꺼
Ratio = [] #비를 저장함

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
    result = pd.Series()
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

def Portfolio_Result(Ratio_fix: list,start_money: int):
    result = pd.Series()
    for i in range(len(BT_Result_ALL[0])):
        temp = 0
        for j in range(len(BT_Result_ALL)):
            temp += (BT_Result_ALL[j][i] * Ratio_fix[j])/100
        result[str(BT_Result_ALL[0].index[i])] = temp
    return result

def MDD(Ratio_fix,Stock_Data_Close) -> float:
    Make_Index = pd.Series()
    for i in range(len(Stock_Data_Close[0])):
        temp = 0
        for j in range(len(Stock_Data_Close)):
            temp += (Stock_Data_Close[j][i] * Ratio_fix[j])/100
        Make_Index[str(Stock_Data_Close[0].index[i])[:-9]] = temp
    window = 250
    peak = Make_Index.rolling(window,min_periods = 1).max()
    drawdown = Make_Index/peak - 1.0
    max_dd = drawdown.rolling(window,min_periods=1).min()
    return max_dd.min()*100

def Make_Ratio(Portfolio_Stock: list):
    Ratio = [0 for _ in range(len(Portfolio_Stock))]
    accuracy = 10
    jmp = 1
    max_profit = 0
    max_portfolio = [0 for _ in range(len(Portfolio_Stock))]
    min_mdd = -100
    min_mdd_portfolio = [0 for _ in range(len(Portfolio_Stock))]
    for r1 in range(1,accuracy,jmp):
        for r2 in range(1,accuracy,jmp):
            for r3 in range(1,accuracy,jmp):
                for r4 in range(1,accuracy,jmp):
                    for r5 in range(1,accuracy,jmp):
                        Ratio = [r1,r2,r3,r4,r5]
                        for i in range(len(Portfolio_Stock)):
                            if Portfolio_Stock[i][1]==0:
                                Ratio[i] = 0
                        Ratio_fix = [(r/sum(Ratio))*100 for r in Ratio]
                        if (max(Ratio_fix)>30): continue
                        result = Portfolio_Result(Ratio_fix,start_money)
                        MDD_result = MDD(Ratio_fix,Stock_Data_Close)


                        if (result.mean() > max_profit):
                            max_profit = result.mean()
                            max_portfolio = Ratio_fix
                            print("="*80)
                            print("<수익률이 가장 큰 포트폴리오>")
                            print("과거 1년 최대 수익률 : {0:2.3f} %를 기록한 최상의 포트폴리오 발견".format(result.max()))
                            print("과거 1년 최저 수익률 : {0:2.3f} %를 기록한 최상의 포트폴리오 발견".format(result.min()))
                            print()
                            print("과거 1년 평균 수익률 : {0:2.3f} %를 기록한 최상의 포트폴리오 발견".format(max_profit))
                            print("탐색동안 최대 손실 낙폭 : {0:2.3f} %를 기록하였으니 참고하세요(1년)".format(MDD_result))
                            print()
                            for i in range(len(Portfolio_Stock)):
                                print("{0}의 비율 : {1:2.3f} % ".format(Portfolio_Stock[i][0],Ratio_fix[i]))
                            print("="*80)

                        if (MDD_result > min_mdd):
                            min_mdd = MDD_result
                            min_mdd_portfolio = Ratio_fix
                            print("="*80)
                            print("<MDD가 가장 작은 포트폴리오>")
                            print("과거 1년 최대 수익률 : {0:2.3f} %를 기록한 최상의 포트폴리오 발견".format(result.max()))
                            print("과거 1년 최저 수익률 : {0:2.3f} %를 기록한 최상의 포트폴리오 발견".format(result.min()))
                            print()
                            print("과거 1년 평균 수익률 : {0:2.3f} %를 기록한 최상의 포트폴리오 발견".format(max_profit))
                            print("탐색동안 최대 손실 낙폭 : {0:2.3f} %를 기록하였으니 참고하세요(1년)".format(MDD_result))
                            print()
                            for i in range(len(Portfolio_Stock)):
                                print("{0}의 비율 : {1:2.3f} % ".format(Portfolio_Stock[i][0],Ratio_fix[i]))
                            print("="*80)
    return [max_profit,max_portfolio]

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

    Portfolio_Stock = Portfolio_Include(Stock_Data_Close_Today, Stock_Code, DCF_Result, Cutline_Percent)
    print(Portfolio_Stock)
    for i in range(len(Stock_Code)):
        print('='*80)
        print('종목코드 : {0}의 백테스팅 시작'.format(Stock_Code[i][0]))
        BT_result = BackTesting(Stock_Data_Close[i], BackTesting_Term,Can_Sell,Sell_Percent)
        BT_Result_ALL.append(BT_result)
    #print(BT_Result_ALL)
    #Make_BT_Graph(BT_Result_ALL)
    End_Result = Make_Ratio(Portfolio_Stock)
    Stock_Info_txt.close()

if __name__ == '__main__':
    main()
