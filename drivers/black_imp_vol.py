import os
import pandas as pd

from src.black_imp_vol import (
    black_call_iv,
    brent_solver,
)


ticker = "SPY"

expiry = "2026-08-21"

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
        compute Black implied volatilities from market call prices
        and append them to the hedge output table

    inputs
        none

    returns
        none
    '''

    hedge_table = pd.read_csv(
        input_file,
    )

    n_options = len(
        hedge_table,
    )

    black_imp_vol_arr = []

    for i in range(n_options):

        price = hedge_table["mid"].values[i]

        f = hedge_table["spot"].values[i]

        k = hedge_table["strike"].values[i]

        t = hedge_table["t"].values[i]

        df = hedge_table["df"].values[i]

        black_imp_vol = black_call_iv(
            price,
            f,
            k,
            t,
            df,
            brent_solver,
        )

        black_imp_vol_arr.append(
            black_imp_vol,
        )

    hedge_table[
        "black_imp_vol"
    ] = black_imp_vol_arr

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
        hedge_table.head(),
    )

    print(
        "saved to",
        output_file,
    )


if __name__ == "__main__":

    main()