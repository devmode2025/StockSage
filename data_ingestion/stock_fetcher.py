import yfinance as yf
import pandas as pd
import time
from datetime import datetime
from tabulate import tabulate

STOCKS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META",
    "TSLA", "NVDA", "JPM", "V", "WMT"
]

def fetch_stock_prices(stocks=STOCKS, interval="1m", max_retries=3):
    """Fetch stock data with retry logic."""
    data = pd.DataFrame()
    
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}/{max_retries} at {datetime.now()}")
            data = yf.download(
                tickers=stocks,
                period="1d",
                interval=interval,
                group_by='ticker',
                progress=False,
                threads=True
            )
            if not data.empty:
                break
        except Exception as e:
            print(f"Error: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                
    return data

if __name__ == "__main__":
    df = fetch_stock_prices()
    if not df.empty:
        df.to_csv("latest_stocks.csv")
        print("Saved to latest_stocks.csv")
    else:
        print("Failed to fetch data after retries")
        print("Possible solutions:")
        print("1. Check your internet connection")
        print("2. Try again later (Yahoo Finance may be rate limiting)")
        print("3. Use fewer stocks or a longer interval")