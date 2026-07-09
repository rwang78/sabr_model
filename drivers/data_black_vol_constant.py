import os
import pandas as pd

from src.black_vol_constant import black_constant_vol


ticker = "SPY"

history_file = (
    "data/"
    "SPY_history.csv"
)

input_file = (
    "results/tables/"
    "SPY_2026-08-21_hedge_output.csv"
)

output_file = (
    "results/tables/"
    "SPY_2026-08-21_hedge_output.csv"
)


def main():
    '''
    routine use
        compute constant Black volatility and append it to hedge output table

    inputs
        none

    returns
        none
    '''

    history_table = pd.read_csv(
        history_file,
    )

    hedge_table = pd.read_csv(
        input_file,
    )

    close_arr = pd.to_numeric(
        history_table["Close"],
        errors="coerce",
    )

    close_arr = close_arr.dropna()

    price_arr = close_arr.values

    sigma = black_constant_vol(
        price_arr,
    )

    hedge_table["black_constant_vol"] = sigma

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

    print(
        hedge_table.head()
    )

    print(
        "black_constant_vol =",
        sigma,
    )

    print(
        "saved to",
        output_file,
    )


if __name__ == "__main__":

    main()

'''
  ticker      expiry option_type        spot  ...  black_hedge_error  sabr_mc_call  sabr_hedge_value_mean  black_constant_vol
0    SPY  2026-08-21        call  751.280029  ...                NaN    162.244914             151.442237            0.125366
1    SPY  2026-08-21        call  751.280029  ...                NaN    153.129879             146.354825            0.125366
2    SPY  2026-08-21        call  751.280029  ...                NaN    129.974094             141.150469            0.125366
3    SPY  2026-08-21        call  751.280029  ...           0.073509    155.748073             136.464695            0.125366
4    SPY  2026-08-21        call  751.280029  ...           0.142946    148.239923             131.649870            0.125366

[5 rows x 28 columns]
black_constant_vol = 0.1253660312984122
saved to results/tables/SPY_2026-08-21_hedge_output.csv
'''