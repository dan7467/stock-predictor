# Importing necessary libraries
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

def create_training_data(data, time_step=10):
    X, y = [], []
    for i in range(len(data) - time_step - 1):
        X.append(data[i:i + time_step, :])
        y.append(data[i + time_step, 0])
    return np.array(X), np.array(y)

data = pd.DataFrame({
    'Close_Price': np.linspace(100, 300, 500) + 500 * 10,
    'Stock_Volume': np.linspace(10000, 50000, 500),
    'Moving_Average': np.linspace(110, 290, 500)
})

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data[['Close_Price', 'Stock_Volume', 'Moving_Average']])

TIME_STEP = 20
X_train, y_train = create_training_data(scaled_data, TIME_STEP)
X_train = X_train.reshape(X_train.shape[0], TIME_STEP, 3)
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(TIME_STEP, 3), name="LSTM_Layer1"),
    Dropout(0.2, name="Dropout_Regularization1"),
    LSTM(50, return_sequences=False, name="LSTM_Layer2"),
    Dense(25, activation='relu', name="Hidden_Layer"),
    Dense(1, name="Output_Layer")  # Predicting Close_Price
])
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
EPOCHS = 100
BATCH_SIZE = 32
history = model.fit(X_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=1)
test_input = scaled_data[-TIME_STEP:]
test_input = test_input.reshape(1, TIME_STEP, 3)
predicted_close_price = model.predict(test_input)
predicted_close_price = scaler.inverse_transform(
    np.concatenate((predicted_close_price, np.zeros((1, 2))), axis=1)
)[0, 0]

print(f"Predicted Next Day Close_Price: ${predicted_close_price:.2f}")

plt.figure(figsize=(10, 6))
plt.plot(data['Close_Price'], label='Historical Close Price', color='blue')
plt.scatter(len(data), predicted_close_price, color='red', label='Predicted Close Price')
plt.title("Stock Close_Price Prediction using LSTM Model")
plt.xlabel("Time")
plt.ylabel("Close Price")
plt.legend()
plt.show()
