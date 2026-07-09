import os
import numpy as np
import pandas as pd


ticker = "SPY"

expiry = "2026-08-21"

spot = 751.280029296875

t = 0.1232876712328767

r = 0.0

input_file = (
    "data/"
    "SPY_2026-08-21_filtered_option_chain.csv"
)

output_file = (
    "data/"
    "SPY_2026-08-21_hedge_input.csv"
)

# save only columns need to evaluate hedge & hedge errors 

def build_hedge_input_table(
    ticker,
    expiry,
    spot,
    t,
    r,
    input_file,
    output_file,
):
    '''
    Routine Use
        Build a clean option input table for hedge error computation.

    Inputs
        ticker: string, underlying ticker
        expiry: string, option expiration date
        spot: scalar, current underlying price
        t: scalar, time to expiration
        r: scalar, continuously compounded interest rate
        input_file: string, input option chain csv file
        output_file: string, output hedge input csv file

    Returns
        hedge_table: dataframe, cleaned hedge input table
    '''

    option_table = pd.read_csv(
        input_file,
    )

    n_options = len(option_table)

    df = np.exp(
        -r*t
    )

    hedge_table = pd.DataFrame()

    hedge_table["ticker"] = [
        ticker
    ]*n_options

    hedge_table["expiry"] = [
        expiry
    ]*n_options

    hedge_table["option_type"] = [
        "call"
    ]*n_options

    hedge_table["spot"] = [
        spot
    ]*n_options

    hedge_table["strike"] = option_table["strike"].values

    hedge_table["mid"] = option_table["mid"].values

    hedge_table["t"] = [
        t
    ]*n_options

    hedge_table["r"] = [
        r
    ]*n_options

    hedge_table["df"] = [
        df
    ]*n_options

    output_dir = os.path.dirname(
        output_file,
    )

    if output_dir != "":
        os.makedirs(
            output_dir,
            exist_ok=True,
        )

    hedge_table.to_csv(
        output_file,
        index=False,
    )

    return hedge_table


def main():
    '''
    Routine Use
        Generate hedge input csv file.

    Inputs
        None

    Returns
        None
    '''

    hedge_table = build_hedge_input_table(
        ticker,
        expiry,
        spot,
        t,
        r,
        input_file,
        output_file,
    )

    print(
        hedge_table.head()
    )

    print(
        "Saved to",
        output_file,
    )


if __name__ == "__main__":

    main()


'''
  ticker      expiry option_type        spot  strike      mid         t    r   df
0    SPY  2026-08-21        call  751.280029   600.0  151.240  0.123288  0.0  1.0
1    SPY  2026-08-21        call  751.280029   605.0  146.245  0.123288  0.0  1.0
2    SPY  2026-08-21        call  751.280029   610.0  140.995  0.123288  0.0  1.0
3    SPY  2026-08-21        call  751.280029   615.0  136.435  0.123288  0.0  1.0
4    SPY  2026-08-21        call  751.280029   620.0  131.740  0.123288  0.0  1.0
Saved to data/SPY_2026-08-21_hedge_input.csv
'''