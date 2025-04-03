# Nifty 50 Stock Analysis

## Overview
This script fetches and analyzes stock data from the Nifty 50 index using the NSE India API. It identifies top gainers, losers, and stocks with significant price movements relative to their 52-week highs and lows.

## Features
- Fetches real-time stock data from NSE India.
- Identifies the top 5 gainers and losers based on percentage change.
- Determines stocks trading 30% below their 52-week high.
- Finds stocks trading 20% above their 52-week low.
- Analyzes stocks with the highest returns in the last 30 days.
- Visualizes the top 5 gainers and losers using a bar chart.

## Requirements
- Python 3.x
- Required libraries:
  - `requests`
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `time`

Install dependencies using:
```bash
pip install requests pandas matplotlib seaborn
```

## Usage
Run the script using:
```bash
python script.py
```

## How It Works
1. The script sends a request to the NSE India API to fetch stock data.
2. It processes the response, extracting key stock metrics.
3. Data is stored in a Pandas DataFrame for analysis.
4. It calculates percentage changes, 52-week high/low comparisons, and 30-day returns.
5. The top-performing stocks are displayed and plotted using Seaborn.

## Error Handling
- Implements retries for failed API requests due to rate limits or network issues.
- Handles various HTTP response codes (401, 403, 429) with appropriate delays.

## Output
- Console output listing the top 5 gainers, losers, and other analyzed stocks.
- A bar chart visualizing the percentage changes of top gainers and losers.
