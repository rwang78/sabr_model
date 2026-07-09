import os
import pandas as pd

from src.black_call_put_close import black_call


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
        compute SABR call prices from Hagan implied volatilities
        under the Black forward formula and append them to the
        hedge output table

    inputs
        none

    returns
        none
    '''

    hedge_table = pd.read_csv(
        input_file,
    )

    n_options = len(
        hedge_table
    )

    sabr_call_arr = []

    for i in range(n_options):

        f = hedge_table["spot"].values[i]

        k = hedge_table["strike"].values[i]

        sigma = hedge_table["sabr_iv"].values[i]

        t = hedge_table["t"].values[i]

        df = hedge_table["df"].values[i]

        call = black_call(
            f,
            k,
            sigma,
            t,
            df,
        )

        sabr_call_arr.append(
            call
        )

    hedge_table["sabr_call"] = sabr_call_arr

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
        "saved to",
        output_file,
    )


if __name__ == "__main__":

    main()