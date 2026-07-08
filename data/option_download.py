import pandas as pd
import yfinance as yf


def download_option_chain(
    ticker,
    expiry,
):
    '''
    routine use
        download the option chain for a fixed expiration date

    inputs
        ticker: string, ticker symbol
        expiry: string, expiration date

    returns
        spot: scalar, current spot price
        expiry: string, selected expiration date
        t: scalar, time to expiration in years
        option_table: dataframe, call option data
    '''

    stock = yf.Ticker(
        ticker,
    )

    spot = stock.history(
        period="1d",
    )["Close"].iloc[-1]

    expiry_arr = stock.options

    if expiry not in expiry_arr:

        print("available expirations:")
        print(expiry_arr)

        raise ValueError(
            "expiration date is not available"
        )

    today = pd.Timestamp.today()

    expiry_date = pd.Timestamp(
        expiry,
    )

    t = (
        expiry_date - today
    ).days/365.0

    option_chain = stock.option_chain(
        expiry,
    )

    option_table = option_chain.calls.copy()

    option_table["mid"] = (
        option_table["bid"]
        + option_table["ask"]
    )/2.0

    return (
        spot,
        expiry,
        t,
        option_table,
    )