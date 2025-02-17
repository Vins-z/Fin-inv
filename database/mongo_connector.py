from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('mongodb+srv://vinayak7:<db_password>@fintech.e2eup.mongodb.net/'))
db = client['fintech_portfolio']

# Create collections
db.create_collection('users')
db.create_collection('portfolios')
db.create_collection('market_data')
db.create_collection('news_sentiment')

# Insert sample user
db.users.insert_one({
    "username": "testuser",
    "password": "testpassword"  # Use bcrypt in production
})

print("Database initialized successfully!")