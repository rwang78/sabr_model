import os
import pandas as pd

from src.sabr_iv import sabr_iv


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
        compute Hagan SABR implied volatilities from calibrated
        SABR parameters and append them to the hedge output table

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

    sabr_iv_arr = []

    for i in range(n_options):

        s = hedge_table["spot"].values[i]

        k = hedge_table["strike"].values[i]

        t = hedge_table["t"].values[i]

        alpha = hedge_table["sabr_alpha"].values[i]

        beta = hedge_table["sabr_beta"].values[i]

        rho = hedge_table["sabr_rho"].values[i]

        nu = hedge_table["sabr_nu"].values[i]

        sigma = sabr_iv(
            s,
            k,
            t,
            alpha,
            beta,
            rho,
            nu,
        )

        sabr_iv_arr.append(
            sigma
        )

    hedge_table["sabr_iv"] = sabr_iv_arr

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