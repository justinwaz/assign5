import streamlit as st
import yfinance as yf
import pandas as pd

# Set the stock ticker and monthly risk-free rate.
ticker = "MSFT"
rf_monthly = 0.0025

# Display the app's heading.
st.title("Microsoft (MSFT) Monthly Sharpe Ratio")
st.write("By Justin Wang")
st.write("Based on five years of monthly stock data.")
st.write("Monthly risk-free rate: 0.25%")

# Download five years of monthly stock prices.
data = yf.download(
    ticker,
    period="5y",
    interval="1mo",
    auto_adjust=True,
    multi_level_index=True,
    progress=False,
)

if data is None or data.empty:
    st.error("No data found for MSFT. Please try again later.")
else:
    # Select Microsoft's closing prices.
    close_prices = data["Close"][ticker]

    # Calculate percentage returns between monthly prices.
    monthly_returns = close_prices.pct_change(
        fill_method=None
    ).dropna()

    # Calculate average excess return and return volatility.
    excess_returns = monthly_returns - rf_monthly
    mean_excess_return = excess_returns.mean()
    std_dev_return = monthly_returns.std()

    # Calculate and display the monthly Sharpe ratio.
    if pd.isna(std_dev_return) or std_dev_return == 0:
        st.error("Not enough valid return data to calculate the ratio.")
    else:
        monthly_sharpe_ratio = mean_excess_return / std_dev_return

        st.metric(
            label="Monthly Sharpe Ratio",
            value=f"{monthly_sharpe_ratio:.3f}",
        )
