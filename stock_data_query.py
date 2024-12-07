import yfinance as yf

class StockData:
    
    def fetch_data(self, ticker, start_date, end_date):
        return yf.download(ticker, start=start_date, end=end_date)
    
    # gather data from yahoo finance:
    def fetch_data_as_list(self, ticker, start_date, end_date, x_axis_property, y_axis_property):
        data_dict_of_two_lists = self.fetch_data(ticker, start_date, end_date)[y_axis_property].reset_index().to_dict(orient='list')
        return list(zip(map(lambda ts: ts.strftime("%m/%d/%Y, %H:%M:%S"), data_dict_of_two_lists[x_axis_property]), data_dict_of_two_lists[ticker]))
    
    def fetch_data_as_dict(self, ticker, start_date, end_date, x_axis_property, y_axis_property):
        data_dict_of_two_lists = self.fetch_data(ticker, start_date, end_date)[y_axis_property].reset_index().to_dict(orient='list')
        return dict(zip(map(lambda ts: ts.strftime("%m/%d/%Y, %H:%M:%S"), data_dict_of_two_lists[x_axis_property]), data_dict_of_two_lists[ticker]))