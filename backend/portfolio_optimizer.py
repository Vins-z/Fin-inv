import numpy as np
import pandas as pd
from pypfopt import EfficientFrontier, objective_functions
from pypfopt import risk_models, expected_returns

class PortfolioOptimizer:
    def __init__(self):
        self.risk_free_rate = 0.02
        
    def optimize(self, historical_data, sentiment_scores):
        # Calculate expected returns
        mu = expected_returns.capm_return(
            historical_data, 
            risk_free_rate=self.risk_free_rate
        )
        
        # Adjust returns with sentiment scores
        mu *= np.array(sentiment_scores) * 2  # Amplify sentiment impact
        
        # Calculate covariance matrix
        S = risk_models.CovarianceShrinkage(historical_data).ledoit_wolf()
        
        # Create efficient frontier
        ef = EfficientFrontier(mu, S)
        ef.add_objective(objective_functions.L2_reg)
        
        # Optimize for maximum Sharpe ratio
        weights = ef.max_sharpe(risk_free_rate=self.risk_free_rate)
        
        return ef.clean_weights()