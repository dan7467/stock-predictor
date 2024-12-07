import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class Plotter:

    def plot(self, data, x, y, stock_name="", includes_prediction=False):
        plt.figure(figsize=(12, 6))
        plt.plot(data.index, data[y], label=stock_name+" Historical Prices", color="blue")
        # if includes_prediction:
        #     plt.axvline(x=pd.Timestamp(data[x]), color="red", linestyle="--", label="Prediction Start (End Date)")
        # plt.plot(prediction_dates, predicted_prices, "g^", label="Predicted Prices")
        plt.xlabel("Date")
        plt.ylabel("Stock Price")
        plt.title(f"{stock_name} Historical and Predicted Stock Prices")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()