import pandas as pd
import FinanceDataReader as fdr
from datetime import datetime

def get_cur(stock_code,excel_name):
    url_tmpl = 'https://finance.naver.com/item/main.nhn?code=%s'
    url = url_tmpl %(stock_code)
    tables = pd.read_html(url,encoding='euc-kr')
    df = tables[3]
    #df.to_excel(excel_name)
    return df

#종목코드, 시작일, 종료일, 몇번째거래일
def get_price(stock_code,start,end,idx):
    df = fdr.DataReader(stock_code, start, end)
    L = df['Close'].to_list()
    return L[idx]

def get_today():
    ans = datetime.today().strftime("%Y-%m-%d")
    return ans
#print(get_price('005930',  '2021-02-01', get_today(),-1)) #현재 종가 가져오기

def get_per(stock_code): #최근 분기 per 가져오기
    table = get_cur(stock_code,'2020.xlsx')
    if str(table.loc[10].to_list()[-1])=='nan': #실적 발표전 예외처리
        return table.loc[10].to_list()[-2]

    return table.loc[10].to_list()[-1]

def average_per(filename:str) -> float:
    f = open(filename, 'r')
    data = f.read()
    L = data.split('\n')
    ans = 0
    for code in L:
        print(code,'의 per 받아오는 중')
        ans += get_per(code)
    f.close()

    return ans/len(L)


def per_valuation(stock_code,filename):
    avg = average_per(filename)
    print("평균 per은",avg)
    per = get_per(stock_code)
    print(str(stock_code),"의 per은",per)
    cur_value = get_price(stock_code,  '2021-02-01', get_today(),-1)
    print(str(stock_code),"의 현재 종가는",cur_value)

    return int(cur_value*avg/per)

Fair_value = per_valuation('035720',"target_comp.txt")
print("적정주가는 ",Fair_value)
