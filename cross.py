import binance.client as bc
from datetime import datetime, timedelta

# API Binance
api_key = ""
api_secret = ""

# Create Binance client
client = bc.Client(api_key, api_secret)

# Parameters for moving averages and interval
short_period = 7
long_period = 14
interval = "1h"  # Adjust as needed (e.g., "4h", "1d")

# Function to retrieve list of futures symbols
def get_futures_symbols():
    """Fetches available futures symbols from Binance exchange info."""
    exchange_info = client.futures_exchange_info()
    symbols = [symbol['symbol'] for symbol in exchange_info['symbols']]
    return symbols

# Get list of futures symbols
futures_symbols = get_futures_symbols()

# Function to scan a single futures pair with optional start date
def scan_futures_pair(symbol, start_date=None):
    """Analyzes a futures pair using moving averages and prints potential signals."""
    try:
        # Construct a start date string (optional)
        if start_date:
            start_str = start_date.strftime("%Y-%m-%dT%H:%M:%S")  # Adjust format if needed

        # Obtain historical klines data
        candlesticks = client.futures_historical_klines(
            symbol, interval, limit=100, start_str=start_str  # Add start_str if provided
        )

        # Handle case with insufficient data
        if len(candlesticks) < 100:
            print(f"Insufficient data for {symbol}. Skipping...")
            return

        # Calculate moving averages
        closing_prices = [float(candle[4]) for candle in candlesticks]  # Extract closing prices
        short_ma = sum(closing_prices[-short_period:]) / short_period
        long_ma = sum(closing_prices[-long_period:]) / long_period

        # Get latest closing price
        latest_price = float(candlesticks[-1][4])

        # Identify potential trading signals
        buy_signal = short_ma > long_ma and latest_price > short_ma
        sell_signal = short_ma < long_ma and latest_price < long_ma

        # Print results
        print(f"Pair: {symbol}")
        print(f"Latest Price: {latest_price}")
        print(f"Short MA ({short_period}): {short_ma}")
        print(f"Long MA ({long_period}): {long_ma}")
        if buy_signal:
            print("**Potential Buy Signal**")
        elif sell_signal:
            print("**Potential Sell Signal**")
        else:
            print("No Signal")
        print("------------------")
    except Exception as e:
        print(f"Error processing symbol {symbol}: {e}")  # Handle potential errors

# Choose a starting date (optional)
# You can comment out this line if you want to retrieve data for the
# most recent period
start_date = datetime.now() - timedelta(days=7)  # Example: Look back 7 days

# Scan all futures symbols
for symbol in futures_symbols:
    scan_futures_pair(symbol, start_date=start_date)  # Pass optional start date