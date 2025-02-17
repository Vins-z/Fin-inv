from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from pymongo import MongoClient
from data_fetcher import DataFetcher
from portfolio_optimizer import PortfolioOptimizer
from backtester import Backtester
from ml_models import PricePredictor, SentimentAnalyzer
import jwt
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Database Connection
client = MongoClient(os.getenv('MONGO_URI'))
db = client[os.getenv('DB_NAME')]

# Initialize Modules
data_fetcher = DataFetcher()
optimizer = PortfolioOptimizer()
backtester = Backtester()
predictor = PricePredictor()
sentiment_analyzer = SentimentAnalyzer()

@app.route('/api/optimize', methods=['POST'])
def optimize():
    data = request.json
    symbols = data['symbols']
    timeframe = data.get('timeframe', '1y')
    
    # Fetch data
    historical_data = data_fetcher.get_historical_data(symbols, timeframe)
    
    # Add sentiment analysis
    sentiment_scores = [data_fetcher.get_sentiment(symbol) for symbol in symbols]
    
    # Optimize portfolio
    weights = optimizer.optimize(historical_data, sentiment_scores)
    
    # Save to database
    db.portfolios.insert_one({
        "timestamp": datetime.datetime.now(),
        "weights": weights,
        "symbols": symbols
    })
    
    return jsonify({"optimized_weights": weights})

@app.route('/api/backtest', methods=['POST'])
def backtest():
    data = request.json
    strategy = data['strategy']
    symbols = data['symbols']
    historical_data = data_fetcher.get_historical_data(symbols)
    
    results = backtester.run_backtest(
        strategy=strategy,
        data=historical_data,
        initial_balance=100000
    )
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)