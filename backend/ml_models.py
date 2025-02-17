import numpy as np
from sklearn.ensemble import RandomForestRegressor
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import pandas as pd

class PricePredictor:
    def __init__(self):
        self.model = self.build_lstm_model()

    def build_lstm_model(self):
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(60, 1)),
            LSTM(50),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        return model

    def train(self, historical_data):
        # Prepare data for LSTM
        X, y = self._prepare_data(historical_data)
        self.model.fit(X, y, epochs=10, batch_size=32)

    def _prepare_data(self, data):
        # Create sequences for LSTM
        X, y = [], []
        for i in range(60, len(data)):
            X.append(data[i-60:i])
            y.append(data[i])
        return np.array(X), np.array(y)

class SentimentAnalyzer:
    def __init__(self):
        from nltk.sentiment import SentimentIntensityAnalyzer
        self.sia = SentimentIntensityAnalyzer()

    def analyze_news(self, text):
        return self.sia.polarity_scores(text)['compound']