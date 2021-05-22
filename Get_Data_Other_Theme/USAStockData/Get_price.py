import pandas as pd
import FinanceDataReader as fdr
from datetime import datetime

def get_price(stock_code,start,end,idx):
    df = fdr.DataReader(stock_code, start, end)
    L = df['Close'].to_list()
    return L[idx]

def get_today():
    ans = datetime.today().strftime("%Y-%m-%d")
    return ans

print(get_price('AAPL',  '2021-02-01', get_today(),-1)) #현재 종가 가져오기
