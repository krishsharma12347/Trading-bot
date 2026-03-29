from binance.client import Client

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

# Connect to Binance Testnet
client = Client(api_key, api_secret, testnet=True)

# Check account balance
balance = client.futures_account_balance()
print(balance)