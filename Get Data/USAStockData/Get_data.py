from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

def get_indicator(stock_symbol, indicator):
    try:
        url = 'http://finviz.com/quote.ashx?t='+stock_symbol.lower()
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'}) #봇을 차단하는 기능 뚫기
        html = urlopen(req).read()
        soup = BeautifulSoup(html, 'lxml')
        ans = soup.find(text=indicator).find_next(class_='snapshot-td2').text
        return ans
    except Exception as e:
        print("에러 : ",e)

psr = get_indicator("AAPL","P/S")
