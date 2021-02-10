import OpenDartReader
import pandas as pd
import openpyxl
api_key = ' ' #인증키 발급받아서 넣어야함
dart = OpenDartReader(api_key)

ex = dart.finstate('삼성전자', 2019, reprt_code='11013') #1분기보고서 19/05
ex.to_excel('11013.xlsx')
ex = dart.finstate('삼성전자', 2019, reprt_code='11012') #반기보고서 19/08
ex.to_excel('11012.xlsx')
ex = dart.finstate('삼성전자', 2019, reprt_code='11014') #3분기보고서 19/11
ex.to_excel('11014.xlsx')
ex = dart.finstate('삼성전자', 2019, reprt_code='11011') #사업보고서 20/03
ex.to_excel('11011.xlsx')
