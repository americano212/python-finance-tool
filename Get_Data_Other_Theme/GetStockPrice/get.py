import FinanceDataReader as fdr
df = fdr.DataReader('005930',  '2020-12-01', '2020-12-30')

#종목코드, 시작일, 종료일, 몇번째거래일
def get_price(stock_code,start,end,idx):
    df = fdr.DataReader(stock_code, start, end)
    L = df['Close'].to_list()
    return L[idx]


print(get_price('005930',  '2020-12-01', '2020-12-30',10))
