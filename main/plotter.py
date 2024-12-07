import matplotlib.colors
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import matplotlib
import pandas as pd
import io
import base64

class Plotter:

    def plot(self, data, x, y, stock_name="", includes_prediction=False, dark_mode="off"):
        curr_theme_colors = {}
        if dark_mode == "on":
            curr_theme_colors['bg'], curr_theme_colors['navbar'], curr_theme_colors['text'] = "#03346E", "#021526", "#E2E2B6"
        else:
            curr_theme_colors['bg'], curr_theme_colors['navbar'], curr_theme_colors['text'] = "#C1BAA1", "#A59D84", "black"
        map(lambda color: mcolors.hex2color(curr_theme_colors[color]), curr_theme_colors)
        curr_theme_colors['axis'] = "white" if dark_mode == "on" else "black"
        curr_theme_colors['plot'] = "orange" if dark_mode == "on" else "blue"
        matplotlib.use('agg')
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.set_facecolor(curr_theme_colors['bg'])
        fig.patch.set_facecolor(curr_theme_colors['bg'])
        ax.plot(data.index, data[y], label=f"{stock_name} Historical Prices", color=curr_theme_colors['plot'])
        # if includes_prediction:
        #     ax.axvline(x=pd.Timestamp(data[x]), color="red", linestyle="--", label="Prediction Start (End Date)")
        #     ax.plot(prediction_dates, predicted_prices, "g^", label="Predicted Prices")
        ax.set_xlabel("Date", color=curr_theme_colors['axis'])
        ax.set_ylabel("Stock Price", color=curr_theme_colors['axis'])
        ax.set_title(f"{stock_name} Historical and Predicted Stock Prices", color=curr_theme_colors['axis'])
        ax.tick_params(colors=curr_theme_colors['axis'])
        plt.xticks(rotation=45)
        plt.tight_layout()
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plt.close()

        return base64.b64encode(image_png).decode('utf-8')