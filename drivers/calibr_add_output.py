import os
import pandas as pd


ticker = "SPY"

expiry = "2026-08-21"

beta_case = 0.5

input_file = (
    "results/tables/"
    "SPY_2026-08-21_hedge_output.csv"
)

param_file = (
    "results/tables/"
    "SPY_2026-08-21_sabr_params.csv"
)

output_file = (
    "results/tables/"
    "SPY_2026-08-21_hedge_output.csv"
)


def main():
    '''
    routine use
        add selected calibrated SABR parameter set to hedge output table

    inputs
        none

    returns
        none
    '''

    hedge_table = pd.read_csv(
        input_file,
    )

    param_table = pd.read_csv(
        param_file,
    )

    param_row = param_table[
        param_table["beta"] == beta_case
    ].iloc[0]

    hedge_table["sabr_beta"] = param_row["beta"]
    hedge_table["sabr_alpha"] = param_row["alpha"]
    hedge_table["sabr_rho"] = param_row["rho"]
    hedge_table["sabr_nu"] = param_row["nu"]
    hedge_table["sabr_sse"] = param_row["sse"]

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
    
    