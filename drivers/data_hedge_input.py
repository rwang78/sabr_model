import os
import numpy as np
import pandas as pd


ticker = "SPY"

expiry = "2026-08-21"

input_file = (
    "data/"
    "SPY_2026-08-21_hedge_input.csv"
)

output_file = (
    "results/tables/"
    "SPY_2026-08-21_hedge_output.csv"
)

r = 0.04


def main():
    '''
    routine use
        copy hedge input table to the results folder
        and add constant interest rate and discount factor

    inputs
        none

    returns
        none
    '''

    hedge_table = pd.read_csv(
        input_file,
    )

    hedge_table["r"] = r

    hedge_table["df"] = np.exp(
        -r*hedge_table["t"]
    )

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