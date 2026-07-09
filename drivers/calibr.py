import os
import numpy as np
import pandas as pd

from src.calibr import sabr_calibr_beta_cases


ticker = "SPY"

expiry = "2026-08-21"

input_file = (
    "results/tables/"
    "SPY_2026-08-21_hedge_output.csv"
)

output_file = (
    "results/tables/"
    "SPY_2026-08-21_sabr_params.csv"
)


def main():
    '''
    routine use
        calibrate SABR alpha, rho, and nu for selected beta values

    inputs
        none

    returns
        none
    '''

    hedge_table = pd.read_csv(
        input_file,
    )

    valid_table = hedge_table.dropna(
        subset=[
            "black_imp_vol",
        ]
    )

    f = valid_table["spot"].values[0]

    t = valid_table["t"].values[0]

    k_arr = valid_table["strike"].values

    iv_arr = valid_table["black_imp_vol"].values

    beta_arr = np.array(
        [
            0.0,
            0.5,
            1.0,
        ]
    )

    alpha_min = 0.001
    alpha_max = 10.0
    n_alpha = 25

    rho_min = -0.99
    rho_max = 0.99
    n_rho = 25

    nu_min = 0.001
    nu_max = 5.0
    n_nu = 25

    results = sabr_calibr_beta_cases(
        f,
        k_arr,
        t,
        iv_arr,
        beta_arr,
        alpha_min,
        alpha_max,
        n_alpha,
        rho_min,
        rho_max,
        n_rho,
        nu_min,
        nu_max,
        n_nu,
    )

    result_table = pd.DataFrame(
        results,
        columns=[
            "beta",
            "alpha",
            "rho",
            "nu",
            "sse",
        ],
    )

    result_table.insert(
        0,
        "expiry",
        expiry,
    )

    result_table.insert(
        0,
        "ticker",
        ticker,
    )

    output_dir = os.path.dirname(
        output_file,
    )

    if output_dir != "":
        os.makedirs(
            output_dir,
            exist_ok=True,
        )

    result_table.to_csv(
        output_file,
        index=False,
    )

    print(
        result_table,
    )

    print(
        "saved to",
        output_file,
    )


if __name__ == "__main__":

    main()


'''
  ticker      expiry  beta      alpha     rho        nu       sse
0    SPY  2026-08-21   0.0  10.000000 -0.2475  5.000000  0.839690
1    SPY  2026-08-21   0.5   3.750625 -0.5775  1.875625  0.007951
2    SPY  2026-08-21   1.0   6.250375 -0.9900  4.583417  0.281282
saved to results/tables/SPY_2026-08-21_sabr_params.csv

~ 2min
'''