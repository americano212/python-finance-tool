import FinanceDataReader as fdr
# pip install -U finance-datareader

df = fdr.DataReader('USD/KRW', '2010')
print(df)
