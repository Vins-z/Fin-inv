import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

    # MongoDB Configuration
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
    DB_NAME = os.getenv('DB_NAME', 'fintech_portfolio')

    # API Keys
    ALPHA_VANTAGE_KEY = os.getenv('ALPHA_VANTAGE_KEY')
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')

    # Machine Learning Configuration
    ML_MODEL_PATH = os.getenv('ML_MODEL_PATH', 'models/portfolio_model.h5')
    SENTIMENT_MODEL_PATH = os.getenv('SENTIMENT_MODEL_PATH', 'models/sentiment_model.pkl')

    # Backtesting Configuration
    INITIAL_BALANCE = float(os.getenv('INITIAL_BALANCE', '100000'))
    RISK_FREE_RATE = float(os.getenv('RISK_FREE_RATE', '0.02'))

    # Frontend Configuration
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')

# Export configuration
settings = Config()