import pandas as pd

def get_cur(stock_code,excel_name):
    url_tmpl = 'https://finance.naver.com/item/main.nhn?code=%s'
    url = url_tmpl %(stock_code)
    tables = pd.read_html(url,encoding='euc-kr')
    df = tables[3]
    df.to_excel(excel_name)

get_cur('005930','2020.xlsx')
