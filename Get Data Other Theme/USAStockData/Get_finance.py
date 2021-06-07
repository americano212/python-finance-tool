import FundamentalAnalysis as fa


ticker = "AAPL"
api_key = "67e344e5fb080276a5432665653ccf32"


# Collect the Balance Sheet statements
#balance_sheet_annually = fa.balance_sheet_statement(ticker, api_key, period="annual")
#balance_sheet_quarterly = fa.balance_sheet_statement(ticker, api_key, period="quarter")
# Collect the Income Statements
#income_statement_annually = fa.income_statement(ticker, api_key, period="annual")
income_statement_quarterly = fa.income_statement(ticker, api_key, period="quarter")
income_statement_quarterly.to_excel('C:\\Users\\ShinDongJun\\Desktop\\PythonStockTool\\USAStockData\\qwe.xlsx')
# Collect the Cash Flow Statements
#cash_flow_statement_annually = fa.cash_flow_statement(ticker, api_key, period="annual")
#cash_flow_statement_quarterly = fa.cash_flow_statement(ticker, api_key, period="quarter")
