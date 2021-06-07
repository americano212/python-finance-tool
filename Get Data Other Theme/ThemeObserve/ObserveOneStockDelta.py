import pandas as pd
import FinanceDataReader as fdr
from datetime import datetime

def get_today():
    ans = datetime.today().strftime("%Y-%m-%d")
    return ans

def OneStockDelta(stock_code,start,end):
    df = fdr.DataReader(stock_code, start, end)
    L = df['Close'].to_list()
    return (L[-1]-L[-2])*100/L[-2]

print(OneStockDelta('AAPL','2021-03-01',get_today()))
