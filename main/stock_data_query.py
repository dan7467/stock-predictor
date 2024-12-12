import yfinance as yf
import pandas as pd
from datetime import datetime
import math

class StockData:
    
    def __init__(self):
        self.resolution = 100
        self.interval_vals = [390, 195, 78, 26, 13, 7, 1, 0.2, 0.14, 0.03, 0.01]
        self.interval_keys = ["1m", "2m", "5m", "15m", "30m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]
        
    def getIntervalFromNumOfYears(self, years):
        if years > 18:
            return "3mo"
        elif years > 5:
            return "1mo"
        else:
            return "1wk"
        
    def fetch_company_info(self, ticker):
        return yf.Ticker(ticker).info
            
    def fetch_data(self, ticker, start_date, end_date):
        first_trade_epoch_utc_date = int(self.fetch_company_info(ticker)['firstTradeDateEpochUtc'])
        total_days = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days
        if total_days < 1:
            return self.fetch_current_day_stock_info(ticker)
        if 1 <= total_days < 32:
            return yf.download(ticker, start=start_date, end=end_date, interval="1h")
        if total_days > self.resolution:
            return yf.download(ticker, start=start_date, end=end_date, interval=self.calc_resolution(total_days))
        return yf.download(ticker, start=start_date, end=end_date)
    
    def fetch_all_stock_data(self, ticker):
        first_trade_epoch_utc_date = int(self.fetch_company_info(ticker)['firstTradeDateEpochUtc'])
        date_diff_in_years = (datetime.now() - datetime.fromtimestamp(first_trade_epoch_utc_date)).days / 365.25
        return yf.download(ticker, period="max", auto_adjust=False, interval=self.getIntervalFromNumOfYears(date_diff_in_years))
    
    def check_if_symbol_exists(self, ticker):
        data = self.fetch_all_stock_data(ticker)  # TO-DO: change fetch_all_stock_data into something more efficient.
                                                    # it's wasteful to query ALL of the data for each symbol-existence check.
        return len(data) != 0 and not (data is pd.DataFrame and data.empty)
    
    def fetch_current_day_stock_info(self, ticker):
        data = yf.download(ticker, period="1d", interval="1m")
        val_dict_len = len(data['Close'])
        if val_dict_len <= self.resolution:
            return data
        interval = math.ceil(val_dict_len / self.resolution)
        data = data.iloc[::interval]  # narrow down to fit resolution
        return data
            
    
    def calc_resolution(self, total_days):
        # for each key k, intervals[k] == approx k to fit in stock-market working hours
        
        # Find the best interval that satisfies resolution
        for i in range(len(self.interval_vals)):
            if total_days * self.interval_vals[i] <= self.resolution:
                return self.interval_keys[i]
    
    # def fetch_data_as_list(self, ticker, start_date, end_date, x_axis_property, y_axis_property):
    #     data_dict_of_two_lists = self.fetch_data(ticker, start_date, end_date)[y_axis_property].reset_index().to_dict(orient='list')
    #     return list(zip(map(lambda ts: ts.strftime("%m/%d/%Y, %H:%M:%S"), data_dict_of_two_lists[x_axis_property]), data_dict_of_two_lists[ticker]))
    
    # def fetch_data_as_dict(self, ticker, start_date, end_date, x_axis_property, y_axis_property):
    #     data_dict_of_two_lists = self.fetch_data(ticker, start_date, end_date)[y_axis_property].reset_index().to_dict(orient='list')
    #     return dict(zip(map(lambda ts: ts.strftime("%m/%d/%Y, %H:%M:%S"), data_dict_of_two_lists[x_axis_property]), data_dict_of_two_lists[ticker]))
    
    
#     Ticker =  yfinance.Ticker object <AAPL>
# Info =  {'address1': 'One Apple Park Way', 'city': 'Cupertino', 'state': 'CA', 'zip': '95014', 'country': 'United States', 'phone': '(408) 996-1010',
# 'website': 'https://www.apple.com', 'industry': 'Consumer Electronics', 'industryKey': 'consumer-electronics', 'industryDisp': 'Consumer Electronics',
# 'sector': 'Technology', 'sectorKey': 'technology', 'sectorDisp': 'Technology',
# 
# 'longBusinessSummary': 'Apple Inc. designs, manufactures, and markets 
# smartphones, personal computers, tablets, wearables, and accessories worldwide. The company offers iPhone, a line of smartphones; Mac, a line of personal
# computers; iPad, a line of multi-purpose tablets; and wearables, home, and accessories comprising AirPods, Apple TV, Apple Watch, Beats products, and 
# HomePod. It also provides AppleCare support and cloud services; and operates various platforms, including the App Store that allow customers 
# to discover and download applications and digital content, such as books, music, video, games, and podcasts, as well as advertising services 
# include third-party licensing arrangements and its own advertising platforms. In addition, the company offers various subscription-based services,
# such as Apple Arcade, a game subscription service; Apple Fitness+, a personalized fitness service; Apple Music, which offers users a curated 
# listening experience with on-demand radio stations; Apple News+, a subscription news and magazine service; Apple TV+, which offers exclusive
# original content; Apple Card, a co-branded credit card; and Apple Pay, a cashless payment service, as well as licenses its intellectual property. 
# The company serves consumers, and small and mid-sized businesses; and the education, enterprise, and government markets. It distributes third-party
# applications for its products through the App Store. The company also sells its products through its retail and online stores, and direct sales force;
# and third-party cellular network carriers, wholesalers, retailers, and resellers. Apple Inc. was founded in 1976 and is headquartered in Cupertino,
# California.',
# 
# 'fullTimeEmployees': 164000, 'companyOfficers':
# [{'maxAge': 1, 'name': 'Mr. # Timothy D. Cook', 'age': 62, 'title': 'CEO & Director', 'yearBorn': 1961, 'fiscalYear': 2023, 'totalPay': 16239562, 'exercisedValue': 0, 'unexercisedValue': 0},
# {'maxAge': 1, 'name': 'Mr. Luca  Maestri', 'age': 60, 'title': 'CFO & Senior VP', 'yearBorn': 1963, 'fiscalYear': 2023, 'totalPay': 4612242, 'exercisedValue': 0, 'unexercisedValue': 0},
# {'maxAge': 1, 'name': 'Mr. Jeffrey E. Williams', 'age': 59, 'title': 'Chief Operating Officer', 'yearBorn': 1964, 'fiscalYear': 2023, 'totalPay': 4637585, 'exercisedValue': 0, 'unexercisedValue': 0},
# {'maxAge': 1, 'name': 'Ms. Katherine L. Adams', 'age': 59, 'title': 'Senior VP, General Counsel & Secretary', 'yearBorn': 1964, 'fiscalYear': 2023, 'totalPay': 4618064, 'exercisedValue': 0, 'unexercisedValue': 0},
# {'maxAge': 1, 'name': "Ms. Deirdre  O'Brien", 'age': 56, 'title': 'Chief People Officer & Senior VP of Retail', 'yearBorn': 1967, 'fiscalYear': 2023, 'totalPay': 4613369, 'exercisedValue': 0, 'unexercisedValue': 0},
# {'maxAge': 1, 'name': 'Mr. Chris  Kondo', 'title': 'Senior Director of Corporate Accounting', 'fiscalYear': 2023, 'exercisedValue': 0, 'unexercisedValue': 0},
# {'maxAge': 1, 'name': 'Suhasini  Chandramouli', 'title': 'Director of Investor Relations', 'fiscalYear': 2023, 'exercisedValue': 0, 'unexercisedValue': 0},
# {'maxAge': 1, 'name': 'Mr. Greg  Joswiak', 'title': 'Senior Vice President of Worldwide Marketing', 'fiscalYear': 2023, 'exercisedValue': 0, 'unexercisedValue': 0},
# {'maxAge': 1, 'name': 'Mr. Adrian  Perica', 'age': 49, 'title': 'Head of Corporate Development', 'yearBorn': 1974, 'fiscalYear': 2023, 'exercisedValue': 0, 'unexercisedValue': 0},
# {'maxAge': 1, 'name': 'Mr. Michael  Fenger', 'title': 'VP of Worldwide Sales', 'fiscalYear': 2023, 'exercisedValue': 0, 'unexercisedValue': 0}],
# 
# 'auditRisk': 6, 'boardRisk': 1, 'compensationRisk': 2, 'shareHolderRightsRisk': 1, 'overallRisk': 1, 'governanceEpochDate': 1733011200,
# 'compensationAsOfEpochDate': 1703980800, 'irWebsite': 'http://investor.apple.com/', 'maxAge': 86400, 'priceHint': 2, 'previousClose': 247.77,
# 'open': 247.945, 'dayLow': 246.2601, 'dayHigh': 250.8, 'regularMarketPreviousClose': 247.77, 'regularMarketOpen': 247.945,
# 'regularMarketDayLow': 246.2601, 'regularMarketDayHigh': 250.8, 'dividendRate': 1.0, 'dividendYield': 0.004, 'exDividendDate': 1731024000,
# 'payoutRatio': 0.1612, 'fiveYearAvgDividendYield': 0.62, 'beta': 1.24, 'trailingPE': 40.607906, 'forwardPE': 29.748917, 'volume': 42854558,
# 'regularMarketVolume': 42854558, 'averageVolume': 47649192, 'averageVolume10days': 39777550, 'averageDailyVolume10Day': 39777550, 'bid': 246.35,
# 'ask': 246.59, 'bidSize': 800, 'askSize': 400, 'marketCap': 3725893566464, 'fiftyTwoWeekLow': 164.08, 'fiftyTwoWeekHigh': 250.8,
# 'priceToSalesTrailing12Months': 9.528287, 'fiftyDayAverage': 231.063, 'twoHundredDayAverage': 207.9642, 'trailingAnnualDividendRate': 0.98,
# 'trailingAnnualDividendYield': 0.0039552813, 'currency': 'USD', 'enterpriseValue': 3799135551488, 'profitMargins': 0.23971, 'floatShares': 15091184209,
# 'sharesOutstanding': 15115799552, 'sharesShort': 154104746, 'sharesShortPriorMonth': 133040194, 'sharesShortPreviousMonthDate': 1730332800,
# 'dateShortInterest': 1732838400, 'sharesPercentSharesOut': 0.010199999, 'heldPercentInsiders': 0.02056, 'heldPercentInstitutions': 0.61939,
# 'shortRatio': 3.41, 'shortPercentOfFloat': 0.010199999, 'impliedSharesOutstanding': 15332100096, 'bookValue': 3.767, 'priceToBook': 65.43404,
# 'lastFiscalYearEnd': 1727481600, 'nextFiscalYearEnd': 1759017600, 'mostRecentQuarter': 1727481600, 'earningsQuarterlyGrowth': -0.358,
# 'netIncomeToCommon': 93736001536, 'trailingEps': 6.07, 'forwardEps': 8.31, 'lastSplitFactor': '4:1', 'lastSplitDate': 1598832000,
# 'enterpriseToRevenue': 9.716, 'enterpriseToEbitda': 28.213, '52WeekChange': 0.25161648, 'SandP52WeekChange': 0.28208935, 'lastDividendValue': 0.25,
# 'lastDividendDate': 1731024000, 'exchange': 'NMS', 'quoteType': 'EQUITY', 'symbol': 'AAPL', 'underlyingSymbol': 'AAPL', 'shortName': 'Apple Inc.',
# 'longName': 'Apple Inc.', 'firstTradeDateEpochUtc': 345479400, 'timeZoneFullName': 'America/New_York', 'timeZoneShortName': 'EST',
# 'uuid': '8b10e4ae-9eeb-3684-921a-9ab27e4d87aa', 'messageBoardId': 'finmb_24937', 'gmtOffSetMilliseconds': -18000000, 'currentPrice': 246.49,
# 'targetHighPrice': 300.0, 'targetLowPrice': 184.0, 'targetMeanPrice': 244.47739, 'targetMedianPrice': 250.0, 'recommendationMean': 1.89362,
# 'recommendationKey': 'buy', 'numberOfAnalystOpinions': 42, 'totalCash': 65171001344, 'totalCashPerShare': 4.311, 'ebitda': 134660997120,
# 'totalDebt': 119058997248, 'quickRatio': 0.745, 'currentRatio': 0.867, 'totalRevenue': 391034994 42, 'totalCash': 65171001344,
# 'totalCashPerShare': 4.311, 'ebitda': 134660997120, 'totalDebt': 119058997248, 'quickRatio': 0.745, 'currentRatio': 0.867,
# 'totalRevenue': 391034994688, 'debtToEquity': 209.059, 'revenuePerShare': 25.485, 'returnOnAssets': 0.21464, 'returnOnEquity': 1.5741299,
# 'freeCashflow': 110846001152, 'operatingCashflow': 118254002176, 'earningsGrowth': -0.341, 'revenueGrowth': 0.061, 'grossMargins': 0.46206,
# 'ebitdaMargins': 0.34437, 'operatingMargins': 0.31171, 'financialCurrency': 'USD', 'trailingPegRatio': 2.56}