import os
import pandas as pd

from src.black_imp_vol import black_call_iv
from src.black_imp_vol import brent_solver


# market data

ticker = "SPY"

expiry = "2026-08-21"

spot = 751.280029296875

t = 0.1232876712328767

df = 1.0


# input data

input_file = (
    "data/"
    "SPY_2026-08-21_filtered_option_chain.csv"
)


def main():
    '''
    routine use
        compute Black implied volatility from filtered option chain

    inputs
        none

    returns
        none
    '''

    option_table = pd.read_csv(
        input_file,
    )

    n_options = len(
        option_table,
    )

    market_iv_arr = []

    for i in range(n_options):

        k_i = option_table["strike"].values[i]

        price_i = option_table["mid"].values[i]

        iv_i = black_call_iv(
            price_i,
            spot,
            k_i,
            t,
            df,
            brent_solver,
        )

        market_iv_arr.append(
            iv_i,
        )

    option_table["computed_impliedVolatility"] = market_iv_arr

    output_dir = "results/tables"

    os.makedirs(
        output_dir,
        exist_ok=True,
    )

    output_file = (
        output_dir
        + "/"
        + ticker
        + "_"
        + expiry
        + "_computed_iv.csv"
    )

    option_table.to_csv(
        output_file,
        index=False,
    )

    print(
        option_table[
            [
                "strike",
                "mid",
                "impliedVolatility",
                "computed_impliedVolatility",
            ]
        ]
    )

    print()
    print("saved to")
    print(output_file)


if __name__ == "__main__":
    main()


'''
  routines to compute black implied volatility \sigma_market later to use in calibr.py
     strike      mid  impliedVolatility  computed_impliedVolatility
0     600.0  151.240           0.444586                         NaN
1     605.0  146.245           0.435919                         NaN
2     610.0  140.995           0.406744                         NaN
3     615.0  136.435           0.420660                    0.237680
4     620.0  131.740           0.413855                    0.265615
..      ...      ...                ...                         ...
170   855.0    0.045           0.141122                    0.137829
171   860.0    0.035           0.143563                    0.139769
172   870.0    0.035           0.153817                    0.150424
173   880.0    0.025           0.160165                    0.155882
174   890.0    0.025           0.169930                    0.165889

[175 rows x 4 columns]

saved to
results/tables/SPY_2026-08-21_computed_iv.csv
'''