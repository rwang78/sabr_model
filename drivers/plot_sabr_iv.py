import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


ticker = "SPY"

expiry = "2026-08-21"

input_file = (
    "results/tables/"
    "SPY_2026-08-21_hedge_output.csv"
)

output_file = (
    "results/figures/"
    "SPY_2026-08-21_sabr_smiles.png"
)


def main():
    '''
    routine use
        plot market implied volatility and SABR implied volatility
        smile from hedge output table

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
            "strike",
            "black_imp_vol",
            "sabr_iv",
        ]
    )

    valid_table = valid_table.sort_values(
        by="strike",
    )

    strike_arr = valid_table[
        "strike"
    ].values

    market_iv_arr = valid_table[
        "black_imp_vol"
    ].values

    sabr_iv_arr = valid_table[
        "sabr_iv"
    ].values

    beta = valid_table[
        "sabr_beta"
    ].values[0]

    alpha = valid_table[
        "sabr_alpha"
    ].values[0]

    rho = valid_table[
        "sabr_rho"
    ].values[0]

    nu = valid_table[
        "sabr_nu"
    ].values[0]

    sabr_sse = valid_table[
        "sabr_sse"
    ].values[0]

    output_dir = os.path.dirname(
        output_file,
    )

    if output_dir != "":

        os.makedirs(
            output_dir,
            exist_ok=True,
        )

    plt.figure(
        figsize=(
            8,
            6,
        )
    )

    plt.plot(
        strike_arr,
        market_iv_arr,
        marker="o",
        linestyle="",
        label="market implied volatility",
    )

    plt.plot(
        strike_arr,
        sabr_iv_arr,
        marker="o",
        label="sabr implied volatility",
    )

    plt.xlabel(
        "strike"
    )

    plt.ylabel(
        "implied volatility"
    )

    plt.title(
        (
            "SABR smile "
            + ticker
            + " "
            + expiry
            + "\n"
            + "beta="
            + str(round(beta, 4))
            + ", alpha="
            + str(round(alpha, 4))
            + ", rho="
            + str(round(rho, 4))
            + ", nu="
            + str(round(nu, 4))
            + ", sse="
            + str(round(sabr_sse, 6))
        )
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        output_file,
        dpi=300,
    )

    plt.show()

    print(
        "saved figure to",
        output_file,
    )


if __name__ == "__main__":

    main()