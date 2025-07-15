import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import joblib
from sklearn.preprocessing import MinMaxScaler

# Generate Dummy Data (Replace with real network data)
data = np.random.rand(500, 3)  # 500 samples, 3 features (protocol, source_ip length, destination_ip length)

# Normalize Data
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data)

# Save the scaler for later use
joblib.dump(scaler, "scaler.pkl")

# Create LSTM Model
model = Sequential([
    LSTM(50, activation='relu', input_shape=(3, 1)),
    Dense(1, activation='sigmoid')  # Binary classification: normal (0) or threat (1)
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train Model
X_train = scaled_data.reshape(500, 3, 1)  # Reshape for LSTM
y_train = np.random.randint(0, 2, 500)  # Random labels (0 or 1)
model.fit(X_train, y_train, epochs=10, batch_size=32)

# Save Model
model.save("lstm_model.h5")

print("✅ LSTM Model Trained & Saved Successfully!")
