from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime


###################################################################################################################################################

resolution = 100
interval_vals = [390, 195, 78, 26, 13, 7, 1, 0.2, 0.14, 0.03, 0.01]
interval_keys = ["1m", "2m", "5m", "15m", "30m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]
        
def fetch_data(ticker, start_date, end_date):
    # first_trade_epoch_utc_date = int(yf.Ticker(ticker).info['firstTradeDateEpochUtc'])
    # total_days = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days
    # if total_days < 32:
    #     return yf.download(ticker, start=start_date, end=end_date, interval="1h")
    # if total_days > resolution:
    #     return yf.download(ticker, start=start_date, end=end_date, interval=calc_resolution(total_days))
    return yf.download(ticker, start=start_date, end=end_date)

def calc_resolution(total_days):
    for i in range(len(interval_vals)):
        if total_days * interval_vals[i] <= resolution:
            return interval_keys[i]
        
###################################################################################################################################################

df = fetch_data('AAPL', '2010-01-01', '2024-12-12')

# Extract 'Close' data and convert to a DataFrame for compatibility
data = df[['Close']]  # Ensures 'Close' remains a DataFrame

# Convert the DataFrame to a numpy array
dataset = data.values

# Get the number of rows to train the model on
training_data_len = int(np.ceil(len(dataset) * .95))

# Scale the data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)

# Create the training data set
train_data = scaled_data[:training_data_len, :]

# Validate train_data size
if len(train_data) < 60:
    raise ValueError("Not enough data for training. Ensure the dataset is sufficiently large.")

# Split the data into x_train and y_train
x_train, y_train = [], []
for i in range(60, len(train_data)):
    x_train.append(train_data[i-60:i, 0])
    y_train.append(train_data[i, 0])

# Convert to numpy arrays
x_train, y_train = np.array(x_train), np.array(y_train)

# Reshape x_train for LSTM
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

# Build the LSTM model
model = Sequential()
model.add(LSTM(128, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(LSTM(64, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(x_train, y_train, batch_size=1, epochs=1)

# Create the testing data set
test_data = scaled_data[training_data_len - 60:, :]

# Validate test_data size
if len(test_data) < 60:
    raise ValueError("Not enough data for testing. Ensure the dataset is sufficiently large.")

# Split the data into x_test and y_test
x_test = []
y_test = dataset[training_data_len:, :]
for i in range(60, len(test_data)):
    x_test.append(test_data[i-60:i, 0])

# Convert x_test to numpy array and reshape
x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

# Get the model's predicted price values
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

# Calculate the root mean squared error (RMSE)
rmse = np.sqrt(np.mean((predictions - y_test) ** 2))
print(f"RMSE: {rmse}")

# Prepare for plotting
train = data[:training_data_len]
valid = data[training_data_len:].copy()
valid['Predictions'] = predictions

# Plot the data
plt.figure(figsize=(16, 6))
plt.title('Model')
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price USD ($)', fontsize=18)
plt.plot(train, label='Train')
plt.plot(valid[['Close', 'Predictions']], label='Val & Predictions')
plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
plt.show()
