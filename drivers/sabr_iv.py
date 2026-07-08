import pandas as pd

from src.plot_sabr_iv import plot_sabr_smile


param_file = (
    "results/tables/"
    "SPY_2026-08-21_sabr_params_computed_iv.csv"
)

option_file = (
    "results/tables/"
    "SPY_2026-08-21_computed_iv.csv"
)


def main():
    '''
    routine use
        generate SABR volatility smile plots and csv tables for beta cases

    inputs
        none

    returns
        none
    '''

    param_table = pd.read_csv(
        param_file,
    )

    option_table = pd.read_csv(
        option_file,
    )

    option_table = option_table.dropna(
        subset=[
            "computed_impliedVolatility",
        ]
    )

    beta_arr = [
        0.0,
        0.5,
        1.0,
    ]

    for i in range(len(beta_arr)):

        beta_case = beta_arr[i]

        param_row = param_table[
            param_table["beta"] == beta_case
        ].iloc[0]

        print(param_row)

        ticker = param_row["ticker"]
        expiry = param_row["expiry"]

        f = param_row["spot"]
        t = param_row["t"]

        alpha = param_row["alpha"]
        beta = param_row["beta"]
        rho = param_row["rho"]
        nu = param_row["nu"]

        model_name = (
            "beta_"
            + str(beta_case)
        )

        plot_sabr_smile(
            option_table,
            f,
            t,
            alpha,
            beta,
            rho,
            nu,
            ticker,
            expiry,
            model_name,
        )


if __name__ == "__main__":
    main()