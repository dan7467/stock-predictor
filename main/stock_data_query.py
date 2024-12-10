import yfinance as yf
import pandas as pd

class StockData:
    
    def fetch_data(self, ticker, start_date, end_date):
        return yf.download(ticker, start=start_date, end=end_date)
    
    def fetch_data_with_smallest_interval(self, ticker, start_date, end_date):
        return yf.download(ticker, start=start_date, end=end_date, interval="1m")
    
    # fetch maximum data on stock to train Tabular Predictor (still not ready)
    def fetch_all_stock_data(self, ticker):
        return yf.download(ticker, period="max", auto_adjust=False)
    
    def check_if_symbol_exists(self, ticker):
        data = self.fetch_all_stock_data(ticker)
        return len(data) != 0 and not (data is pd.DataFrame and data.empty)
    
    # def fetch_data_as_list(self, ticker, start_date, end_date, x_axis_property, y_axis_property):
    #     data_dict_of_two_lists = self.fetch_data(ticker, start_date, end_date)[y_axis_property].reset_index().to_dict(orient='list')
    #     return list(zip(map(lambda ts: ts.strftime("%m/%d/%Y, %H:%M:%S"), data_dict_of_two_lists[x_axis_property]), data_dict_of_two_lists[ticker]))
    
    # def fetch_data_as_dict(self, ticker, start_date, end_date, x_axis_property, y_axis_property):
    #     data_dict_of_two_lists = self.fetch_data(ticker, start_date, end_date)[y_axis_property].reset_index().to_dict(orient='list')
    #     return dict(zip(map(lambda ts: ts.strftime("%m/%d/%Y, %H:%M:%S"), data_dict_of_two_lists[x_axis_property]), data_dict_of_two_lists[ticker]))
    
    def fetch_current_day_stock_info(self, ticker):
        return yf.Ticker(ticker).history(period="1d", interval="1m")