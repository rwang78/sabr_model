import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.sabr_iv import sabr_iv


def plot_sabr_smile(
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
):
    '''
    routine use
        plot market implied volatility smile and SABR fitted smile

    inputs
        option_table: dataframe, filtered option chain with strike and impliedVolatility columns
        f: scalar, forward price
        t: scalar, time to expiration
        alpha: scalar, SABR volatility level
        beta: scalar, SABR elasticity parameter
        rho: scalar, SABR correlation
        nu: scalar, SABR volatility of volatility
        ticker: string, ticker name
        expiry: string, option expiration date

    returns
        none
    '''

    k_arr = option_table["strike"].values

    market_iv_arr = option_table["impliedVolatility"].values

    sabr_iv_arr = np.zeros(
        len(k_arr)
    )

    for i in range(len(k_arr)):

        sabr_iv_arr[i] = sabr_iv(
            f,
            k_arr[i],
            t,
            alpha,
            beta,
            rho,
            nu,
        )

    table = pd.DataFrame(
        {
            "strike": k_arr,
            "market_iv": market_iv_arr,
            "sabr_iv": sabr_iv_arr,
        }
    )

    table = table.sort_values(
        "strike",
    )

    os.makedirs(
        "results/figures",
        exist_ok=True,
    )

    os.makedirs(
        "results/tables",
        exist_ok=True,
    )

    figure_file = (
        "results/figures/"
        + ticker
        + "_"
        + expiry
        + "_"
        + model_name
        + "_sabr_smile.png"
    )

    csv_file = (
        "results/tables/"
        + ticker
        + "_"
        + expiry
        + "_"
        + model_name
        + "_sabr_smile.csv"
    )

    plt.plot(
        table["strike"],
        table["market_iv"],
        marker="o",
        linestyle="none",
        label="market iv",
    )

    plt.plot(
        table["strike"],
        table["sabr_iv"],
        label="sabr iv",
    )

    plt.xlabel("strike")
    plt.ylabel("implied volatility")
    plt.title(
        ticker
        + " "
        + expiry
        + " volatility smile"
    )

    plt.legend()

    plt.savefig(
        figure_file,
        dpi=300,
        bbox_inches="tight",
    )

    plt.show()

    plt.close()

    table.to_csv(
        csv_file,
        index=False,
    )

    print(
        "saved:",
        figure_file,
    )

    print(
        "saved:",
        csv_file,
    )
