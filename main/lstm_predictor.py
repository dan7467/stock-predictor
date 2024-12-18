from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import tensorflow as tf
from datetime import datetime

###################################################################################################################################################

# # Local testing, model still not generalized:

resolution = 150
interval_vals = [390, 195, 78, 26, 13, 7, 1, 0.2, 0.14, 0.03, 0.01]
interval_keys = ["1m", "2m", "5m", "15m", "30m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]
        
def fetch_data(ticker, start_date, end_date):
    return yf.download(ticker, start=start_date, end=end_date)

def calc_resolution(total_days):
    for i in range(len(interval_vals)):
        if total_days * interval_vals[i] <= resolution:
            return interval_keys[i]
        
###################################################################################################################################################

# configure tensorflow to use GPU
tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(log_device_placement=True))

df = fetch_data('AAPL', '2004-01-01', '2024-12-12')  # train and fetch data

data = df[['Close']]  # extract 'Close' data (price close) and convert to a DataFrame

dataset = data.values # convert DataFrame to a numpy array

training_data_len = int(np.ceil(len(dataset) * .95))

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data[['Close']].values)

training_data_len = int(len(scaled_data) * 0.93)  # Training data length (93%)

train_data = scaled_data[:training_data_len]
test_data = scaled_data[training_data_len - 60:]  # Keep last 60 days as test input

x_train, y_train = [], []
for i in range(60, len(train_data)):
    x_train.append(train_data[i - 60:i, 0])  # Use past 60 days to predict the next value
    y_train.append(train_data[i, 0])

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

model = Sequential()
model.add(LSTM(128, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(LSTM(64, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)  # if the loss function stops improving - early stop

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x_train, y_train, batch_size=32, epochs=40, callbacks=[early_stop])

# predict the next 7% (future prices)
future_predictions = []

# FIXES
input_data = scaler.transform(data['Close'].values[-60:].reshape(-1, 1))

for _ in range(int(len(scaled_data) * 0.07)):  # Predict 7% of the dataset length
    input_reshaped = np.reshape(input_data, (1, input_data.shape[0], 1))
    predicted_value = model.predict(input_reshaped)[0, 0]
    future_predictions.append(predicted_value)
    # update input_data with the predicted value:
    input_data = np.append(input_data, predicted_value)[1:]  # Shift window forward

future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))  # transform predictions back to original scale

# prepare data for visualization
train = data[:training_data_len]
valid = data[training_data_len:]
valid['Predictions'] = np.nan  # No predictions for past validation data

# append future predictions to the dataset for plotting
future_dates = pd.date_range(data.index[-1], periods=len(future_predictions) + 1, freq='B')[1:]
future_df = pd.DataFrame({'Close': np.nan, 'Predictions': future_predictions.flatten()}, index=future_dates)

plt.figure(figsize=(16, 6))
plt.title('Stock Price Prediction Model')
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price USD ($)', fontsize=18)
plt.plot(train['Close'], label='Train Data')
plt.plot(valid['Close'], label='Validation Data (Actual)')
plt.plot(future_df['Predictions'], label='Future Predictions', linestyle='--')
plt.legend()
plt.show()