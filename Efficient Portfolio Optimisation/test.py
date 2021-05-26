from pandas_datareader import data as pdr
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np
yf.pdr_override()
Stock_Code = []
Stock_Data_Close = []
Stock_Data_Close_Today = []
Stock_Name = []
start_ymd = '2020-01-01'
end_ymd = '2021-01-01'
Change_list = []
DCF_Result = []

get_pdr = pdr.get_data_yahoo('{0}.KS'.format('364980'),start='2021-03-05')
print(get_pdr['Close'])
