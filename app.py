from plotter import Plotter
from stock_data_query import StockData

if __name__ == '__main__':
    
    # init facade:
    p = Plotter()
    s = StockData()
    
    # test data:
    ticker = "MSFT"    # <- full list of tickers: https://finance.yahoo.com/lookup/?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAFsJJYhFEqujFuw2R0n2CiVQAK0_waRNPWCiOjt0gRbhQGrPCLcIpM4qHgsbgLgKU95JlF0mrGbxC5NnW-pC0ivmxnofSAEtUKHqJQQZIgjn79KD7zIEfxuOF8FYZnRAIPigowCUklENfdfXeboxR3tdRi3Eq2X-9VxGIr8pNewL
    start_date = "2024-06-01"  # YYYY-MM-DD
    end_date = "2024-12-06"  # YYYY-MM-DD
    x_axis_property = "Date"
    y_axis_property = "Close"
    
    data = s.fetch_data(ticker, start_date, end_date)
    p.plot(data, x_axis_property, y_axis_property, stock_name=ticker, includes_prediction=True)

# # plot results:
# plt.figure(figsize=(12, 6))
# plt.plot(data.index, data["Close"], label=ticker+" Historical Prices", color="blue")
# plt.axvline(x=pd.Timestamp(end_date), color="red", linestyle="--", label="Prediction Start (End Date)")
# # plt.plot(prediction_dates, predicted_prices, "g^", label="Predicted Prices")
# plt.xlabel("Date")
# plt.ylabel("Stock Price")
# plt.title(f"{ticker} - Historical and Predicted Stock Prices")
# plt.legend()
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()
