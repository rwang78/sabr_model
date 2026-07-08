import pandas as pd


csv_file = (
    "data/"
    "SPY_2026-08-21_filtered_option_chain.csv"
)


def load_spy_option_inputs():
    '''
    routine use
        load one SPY option row for monte carlo tests

    inputs
        none

    returns
        f: scalar, forward price
        k: scalar, strike price
        sigma: scalar, implied volatility
        t: scalar, time to expiration
        df: scalar, discount factor
    '''

    table = pd.read_csv(
        csv_file,
    )

    row_id = len(table)//2

    row = table.iloc[row_id]

    f = 751.280029296875
    k = row["strike"]
    sigma = row["impliedVolatility"]
    t = 0.1232876712328767
    df = 1.0

    return f, k, sigma, t, df