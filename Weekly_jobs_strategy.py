from fredapi import Fred
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Api_keys import FRED_API_KEY

# Ensure future warning suppression
pd.set_option('future.no_silent_downcasting', True)

# FRED API setup

fred = Fred(api_key=FRED_API_KEY)

# Function to get real jobless claims data
def get_jobless_claims_data():
    claims = fred.get_series('ICSA').resample('W-FRI').last()
    df = claims.to_frame('Initial Claims')
    df['Claims Change %'] = df['Initial Claims'].pct_change() * 100
    df['Signal'] = np.where(df['Claims Change %'] < -2, 1, np.where(df['Claims Change %'] > 2, 0, np.nan))
    df['Signal'] = df['Signal'].ffill()
    return df

# Robust backtest strategy function
def backtest_strategy(ticker, jobless_claims, spy_cagr):
    try:
        prices = yf.download(ticker,
                             start=jobless_claims.index.min().strftime('%Y-%m-%d'),
                             end=jobless_claims.index.max().strftime('%Y-%m-%d'),
                             auto_adjust=True)['Close'].resample('W-FRI').last()

        # Bulletproof data validation
        if prices.empty or prices.dropna().empty:
            print(f"No valid price data for {ticker}.")
            return None

        df = pd.concat([prices, jobless_claims], axis=1).dropna()
        df.columns = ['Price', 'Initial Claims', 'Claims Change %', 'Signal']

        df['Returns'] = df['Price'].pct_change()
        df['Strategy Returns'] = df['Signal'].shift(1) * df['Returns']

        df['Cumulative Price'] = (1 + df['Returns']).cumprod()
        df['Cumulative Strategy'] = (1 + df['Strategy Returns']).cumprod()

        weeks = len(df)
        strategy_cagr = df['Cumulative Strategy'].iloc[-1] ** (52 / weeks) - 1
        returns = df['Strategy Returns'].dropna()
        sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(52) if returns.std() != 0 else 0
        alpha = strategy_cagr - spy_cagr

        return {
            'df': df,
            'CAGR': strategy_cagr,
            'Sharpe': sharpe_ratio,
            'Alpha': alpha
        }

    except Exception as e:
        print(f"Error with {ticker}: {e}")
        return None

# Main execution
tickers = ['XLY', 'XLF', 'IWM', 'AMZN', 'TSLA', 'HD', 'JPM', 'WFC', 'CAT']
jobless_claims = get_jobless_claims_data()
results = {}

# SPY performance for benchmark
# SPY performance for benchmark
spy_prices = yf.download('SPY',
                         start=jobless_claims.index.min().strftime('%Y-%m-%d'),
                         end=jobless_claims.index.max().strftime('%Y-%m-%d'),
                         auto_adjust=True)['Close'].resample('W-FRI').last().dropna()

spy_returns = spy_prices.pct_change()
spy_cumulative = (1 + spy_returns).cumprod()
weeks_spy = len(spy_cumulative)

# Explicit scalar conversion
spy_cagr = float(spy_cumulative.iloc[-1] ** (52 / weeks_spy) - 1)


# Backtesting loop
for ticker in tickers:
    print(f"Running strategy for {ticker}...")
    result = backtest_strategy(ticker, jobless_claims, spy_cagr)
    if result:
        results[ticker] = result

# Final plotting
plt.figure(figsize=(14, 8))
plt.plot(spy_cumulative, label=f'SPY Buy & Hold (CAGR: {spy_cagr:.2%})', linestyle='--', linewidth=2)

for ticker, data in results.items():
    plt.plot(data['df']['Cumulative Strategy'],
             label=f"{ticker} (α: {data['Alpha']:.2%}, Sharpe: {data['Sharpe']:.2f})")

plt.title('Jobless Claims-Based Strategies vs SPY Buy & Hold\n(Alpha & Sharpe Included)')
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
