import os
import numpy as np
import pandas as pd

from src.black_greeks import black_call_delta
from src.hedge import black_hedge
from src.plot_histogram import plot_hedge_value_histogram


hedge_file = (
    "results/tables/"
    "SPY_2026-08-21_hedge_output.csv"
)

black_path_file = (
    "results/tables/"
    "mc_forward_black_paths_SPY_2026-08-21.csv"
)

sabr_path_file = (
    "results/tables/"
    "mc_forward_sabr_paths_SPY_2026-08-21.csv"
)

output_file = (
    "results/figures/"
    "SPY_2026-08-21_hedge_value_histogram.png"
)


def path_table_to_arr(
    path_table,
    value_column,
):
    '''
    routine use
        convert saved long monte carlo path table to path array

    inputs
        path_table: dataframe, saved path table
        value_column: string, column to convert

    returns
        path_arr: 2d array (n_paths, n_steps + 1), path values
    '''

    path_arr = path_table.pivot(
        index="path_id",
        columns="step",
        values=value_column,
    ).values

    return path_arr


def build_delta_arr(
    path_arr,
    k,
    sigma,
    t,
    df,
):
    '''
    routine use
        compute black forward delta array along simulated paths

    inputs
        path_arr: 2d array (n_paths, n_steps + 1), simulated forward paths
        k: scalar, strike price
        sigma: scalar, volatility used in delta formula
        t: scalar, time to expiration
        df: scalar, discount factor

    returns
        delta_arr: 2d array (n_paths, n_steps), hedge ratios
    '''

    n_paths = path_arr.shape[0]
    n_steps = path_arr.shape[1] - 1

    time_arr = np.linspace(
        0.0,
        t,
        n_steps + 1,
    )

    delta_arr = np.zeros(
        (
            n_paths,
            n_steps,
        )
    )

    for j in range(n_steps):

        t_remaining = t - time_arr[j]

        for i in range(n_paths):

            delta_arr[i, j] = black_call_delta(
                path_arr[i, j],
                k,
                sigma,
                t_remaining,
                df,
            )

    return delta_arr


def main():
    '''
    routine use
        plot histogram of black and sabr hedge values
        using saved monte carlo forward paths

    inputs
        none

    returns
        none
    '''

    hedge_table = pd.read_csv(
        hedge_file,
    )

    black_path_table = pd.read_csv(
        black_path_file,
    )

    sabr_path_table = pd.read_csv(
        sabr_path_file,
    )

    black_path_arr = path_table_to_arr(
        black_path_table,
        "forward",
    )

    sabr_path_arr = path_table_to_arr(
        sabr_path_table,
        "forward",
    )

    spot = hedge_table[
        "spot"
    ].values[0]

    atm_index = np.argmin(
        np.abs(
            hedge_table["strike"].values
            - spot
        )
    )

    hedge_row = hedge_table.iloc[
        atm_index
    ]

    f = hedge_row[
        "spot"
    ]

    k = hedge_row[
        "strike"
    ]

    t = hedge_row[
        "t"
    ]

    df = hedge_row[
        "df"
    ]

    black_sigma = hedge_row[
        "black_constant_vol"
    ]

    sabr_sigma = hedge_row[
        "sabr_iv"
    ]

    black_delta_arr = build_delta_arr(
        black_path_arr,
        k,
        black_sigma,
        t,
        df,
    )

    sabr_delta_arr = build_delta_arr(
        sabr_path_arr,
        k,
        sabr_sigma,
        t,
        df,
    )

    (
        black_hedge_value_arr,
        black_call_payout_arr,
        black_hedge_profit_arr,
        black_hedge_value_mean,
        black_call_price,
        black_hedge_error,
        black_mc_call_price,
        black_price_error,
    ) = black_hedge(
        f,
        k,
        black_sigma,
        t,
        df,
        black_path_arr,
        black_delta_arr,
    )

    (
        sabr_hedge_value_arr,
        sabr_call_payout_arr,
        sabr_hedge_profit_arr,
        sabr_hedge_value_mean,
        sabr_call_price,
        sabr_hedge_error,
        sabr_mc_call_price,
        sabr_price_error,
    ) = black_hedge(
        f,
        k,
        sabr_sigma,
        t,
        df,
        sabr_path_arr,
        sabr_delta_arr,
    )

    output_dir = os.path.dirname(
        output_file,
    )

    if output_dir != "":

        os.makedirs(
            output_dir,
            exist_ok=True,
        )

    plot_hedge_value_histogram(
        black_hedge_value_arr,
        sabr_hedge_value_arr,
        black_call_price,
        sabr_call_price,
        output_file,
    )

    print(
        "strike:",
        k,
    )

    print(
        "black hedge value mean:",
        black_hedge_value_mean,
    )

    print(
        "black call price:",
        black_call_price,
    )

    print(
        "black hedge error:",
        black_hedge_error,
    )

    print(
        "sabr hedge value mean:",
        sabr_hedge_value_mean,
    )

    print(
        "sabr call price:",
        sabr_call_price,
    )

    print(
        "sabr hedge error:",
        sabr_hedge_error,
    )

    print(
        "saved figure to",
        output_file,
    )


if __name__ == "__main__":

    main()