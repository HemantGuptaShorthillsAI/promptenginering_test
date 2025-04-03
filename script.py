import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

# Define the URL for Nifty 50 data
url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050"

# Set up headers
headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.nseindia.com/"
}

# Start a session to manage cookies
session = requests.Session()
session.headers.update(headers)

# Fetch the data
def fetch_nse_data(retries=5, delay=5):
    for attempt in range(retries):
        try:
            response = session.get(url)
            if response.status_code == 200:
                return response.json()
            elif response.status_code in [401, 403, 429]:  # Unauthorized, Forbidden, Too Many Requests
                print(f"Attempt {attempt + 1}: Received {response.status_code}. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"Failed with status code {response.status_code}. Exiting...")
                return None
        except requests.RequestException as e:
            print(f"Error: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
    print("Max retries reached. Could not fetch data.")
    return None

# Fetch the data
data = fetch_nse_data()
if data:
    stocks = data['data']
    
    # Convert data to DataFrame
    df = pd.DataFrame(stocks)

    # Convert relevant columns to float
    df['percentChange'] = df['pChange'].astype(float)
    df['lastPrice'] = df['lastPrice'].astype(float)
    df['high52'] = df['yearHigh'].astype(float)
    df['low52'] = df['yearLow'].astype(float)
    df['previousClose'] = df['previousClose'].astype(float)
    df['change30d'] = df['perChange30d'].astype(float)  # Assuming 'change30d' exists in API

    # Find top 5 gainers and losers
    top_gainers = df.nlargest(5, 'percentChange')[['symbol', 'percentChange']]
    top_losers = df.nsmallest(5, 'percentChange')[['symbol', 'percentChange']]

    # Identify stocks 30% below their 52-week high
    df['percent_below_52w_high'] = ((df['high52'] - df['lastPrice']) / df['high52']) * 100
    below_30_percent = df[df['percent_below_52w_high'] >= 30][['symbol', 'percent_below_52w_high']].nsmallest(5, 'percent_below_52w_high')

    # Identify stocks 20% above their 52-week low
    df['percent_above_52w_low'] = ((df['lastPrice'] - df['low52']) / df['low52']) * 100
    above_20_percent = df[df['percent_above_52w_low'] >= 20][['symbol', 'percent_above_52w_low']].nsmallest(5, 'percent_above_52w_low')

    # Determine stocks with highest returns in last 30 days
    top_30d_returns = df.nlargest(5, 'change30d')[['symbol', 'change30d']]

    # Display results
    print("Top 5 Gainers:")
    print(top_gainers)
    
    print("\nTop 5 Losers:")
    print(top_losers)
    
    print("\nStocks 30% Below 52-Week High:")
    print(below_30_percent)

    print("\nStocks 20% Above 52-Week Low:")
    print(above_20_percent)

    print("\nStocks with Highest Returns in Last 30 Days:")
    print(top_30d_returns)

    plt.figure(figsize=(10, 6))

    # Combine gainers and losers for a single chart
    gainers_losers = pd.concat([top_gainers, top_losers])
    gainers_losers['Type'] = ['Gainer'] * len(top_gainers) + ['Loser'] * len(top_losers)

    # Plot the bar chart
    sns.barplot(x='symbol', y='percentChange', hue='Type', data=gainers_losers, palette={"Gainer": "green", "Loser": "red"})
    
    plt.xlabel("Stock Symbol")
    plt.ylabel("Percentage Change")
    plt.title("Top 5 Gainers & Losers of the Day")
    plt.xticks(rotation=45)
    plt.legend(title="Category")
    plt.show()

else:
    print("Failed to fetch data after multiple attempts.")
