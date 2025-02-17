import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

class Backtester:
    def __init__(self):
        self.scaler = StandardScaler()
        
    def run_backtest(self, strategy, data, initial_balance=100000):
        if strategy == 'ml_strategy':
            return self.ml_strategy(data, initial_balance)
        elif strategy == 'momentum':
            return self.momentum_strategy(data, initial_balance)
        else:
            return self.buy_and_hold(data, initial_balance)

    def ml_strategy(self, data, initial_balance):
        # Feature Engineering
        returns = data.pct_change()
        features = pd.DataFrame({
            'momentum': data.pct_change(30),
            'volatility': returns.rolling(30).std(),
            'volume': data.rolling(30).mean()
        })
        
        # Target: Next day return direction
        target = (data.shift(-1) > data).astype(int)
        
        # Train ML model
        model = LogisticRegression()
        model.fit(self.scaler.fit_transform(features.dropna()), target.dropna())
        
        # Generate signals
        signals = model.predict(features)
        
        # Execute strategy
        positions = np.where(signals == 1, 1, -1)
        portfolio = initial_balance * (1 + (positions * returns)).cumprod()
        
        return {
            'returns': portfolio[-1] / initial_balance - 1,
            'sharpe': self.calculate_sharpe(portfolio)
        }

    def calculate_sharpe(self, returns):
        excess_returns = returns - self.risk_free_rate
        return excess_returns.mean() / excess_returns.std()