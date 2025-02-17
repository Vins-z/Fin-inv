import requests
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from newsapi import NewsApiClient
import os
from dotenv import load_dotenv

load_dotenv()

class DataFetcher:
    def __init__(self):
        self.av_key = os.getenv('ALPHA_VANTAGE_KEY')
        self.news_key = os.getenv('NEWS_API_KEY')
        self.ts = TimeSeries(key=self.av_key)
        self.news_client = NewsApiClient(api_key=self.news_key)

    def get_historical_data(self, symbols, timeframe='1y'):
        data = {}
        for symbol in symbols:
            df, _ = self.ts.get_daily_adjusted(
                symbol=symbol, 
                outputsize='full' if timeframe == 'max' else 'compact'
            )
            data[symbol] = df['5. adjusted close']
        return pd.DataFrame(data).dropna()

    def get_sentiment(self, symbol):
        news = self.news_client.get_everything(
            q=symbol,
            language='en',
            sort_by='relevancy'
        )
        scores = [self._analyze_sentiment(article['title']) 
                 for article in news['articles'][:10]]
        return sum(scores)/len(scores) if scores else 0.5

    def _analyze_sentiment(self, text):
        # Using VADER sentiment analysis
        from nltk.sentiment import SentimentIntensityAnalyzer
        return SentimentIntensityAnalyzer().polarity_scores(text)['compound']