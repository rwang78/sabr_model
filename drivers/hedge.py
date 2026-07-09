import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.black_greeks import black_call_delta
from src.hedge import black_hedge


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
    "results/tables/"
    "SPY_2026-08-21_hedge_output.csv"
)

price_error_figure = (
    "results/figures/"
    "mc_price_error_black_sabr.png"
)

hedge_error_figure = (
    "results/figures/"
    "mc_hedge_error_black_sabr.png"
)


def path_table_to_arr(
    path_table,
    value_column,
):
    '''
    routine use
        convert saved long Monte Carlo path table to path array

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
        compute Black forward delta array along simulated paths

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

        for m in range(n_paths):

            delta_arr[m, j] = black_call_delta(
                path_arr[m, j],
                k,
                sigma,
                t_remaining,
                df,
            )

    return delta_arr


def save_error_plot(
    result_table,
    y_black,
    y_sabr,
    figure_file,
    title,
    ylabel,
):
    '''
    routine use
        save comparison plot for Black and SABR errors

    inputs
        result_table: dataframe, result table
        y_black: string, Black error column
        y_sabr: string, SABR error column
        figure_file: string, output figure file
        title: string, plot title
        ylabel: string, y axis label

    returns
        none
    '''

    valid_table = result_table.dropna(
        subset=[
            y_black,
            y_sabr,
        ]
    )

    figure_dir = os.path.dirname(
        figure_file,
    )

    if figure_dir != "":

        os.makedirs(
            figure_dir,
            exist_ok=True,
        )

    plt.figure()

    plt.plot(
        valid_table["strike"],
        valid_table[y_black],
        marker="o",
        label="black",
    )

    plt.plot(
        valid_table["strike"],
        valid_table[y_sabr],
        marker="o",
        label="sabr",
    )

    plt.xlabel(
        "strike"
    )

    plt.ylabel(
        ylabel
    )

    plt.title(
        title
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        figure_file,
        dpi=300,
    )

    plt.close()


def main():
    '''
    routine use
        compute Monte Carlo price, price error, hedge value,
        and hedge error for Black and SABR under forward framework

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

    n_options = len(
        hedge_table
    )

    result_table = hedge_table.copy()

    black_mc_call_arr = []
    black_price_error_arr = []
    black_hedge_value_mean_arr = []
    black_hedge_error_arr = []
    black_call_payout_mean_arr = []
    black_hedge_profit_mean_arr = []

    sabr_mc_call_arr = []
    sabr_price_error_arr = []
    sabr_hedge_value_mean_arr = []
    sabr_hedge_error_arr = []
    sabr_call_payout_mean_arr = []
    sabr_hedge_profit_mean_arr = []

    for i in range(n_options):

        f = hedge_table["spot"].values[i]
        k = hedge_table["strike"].values[i]
        t = hedge_table["t"].values[i]
        df = hedge_table["df"].values[i]

        black_sigma = hedge_table["black_constant_vol"].values[i]
        sabr_sigma = hedge_table["sabr_iv"].values[i]

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

        black_mc_call_arr.append(
            black_mc_call_price
        )

        black_price_error_arr.append(
            black_price_error
        )

        black_hedge_value_mean_arr.append(
            black_hedge_value_mean
        )

        black_hedge_error_arr.append(
            black_hedge_error
        )

        black_call_payout_mean_arr.append(
            np.mean(
                black_call_payout_arr
            )
        )

        black_hedge_profit_mean_arr.append(
            np.mean(
                black_hedge_profit_arr
            )
        )

        sabr_mc_call_arr.append(
            sabr_mc_call_price
        )

        sabr_price_error_arr.append(
            sabr_price_error
        )

        sabr_hedge_value_mean_arr.append(
            sabr_hedge_value_mean
        )

        sabr_hedge_error_arr.append(
            sabr_hedge_error
        )

        sabr_call_payout_mean_arr.append(
            np.mean(
                sabr_call_payout_arr
            )
        )

        sabr_hedge_profit_mean_arr.append(
            np.mean(
                sabr_hedge_profit_arr
            )
        )

    result_table["black_mc_call"] = black_mc_call_arr
    result_table["black_price_error"] = black_price_error_arr
    result_table["black_hedge_value_mean"] = black_hedge_value_mean_arr
    result_table["black_hedge_error"] = black_hedge_error_arr
    result_table["black_call_payout_mean"] = black_call_payout_mean_arr
    result_table["black_hedge_profit_mean"] = black_hedge_profit_mean_arr

    result_table["sabr_mc_call"] = sabr_mc_call_arr
    result_table["sabr_price_error"] = sabr_price_error_arr
    result_table["sabr_hedge_value_mean"] = sabr_hedge_value_mean_arr
    result_table["sabr_hedge_error"] = sabr_hedge_error_arr
    result_table["sabr_call_payout_mean"] = sabr_call_payout_mean_arr
    result_table["sabr_hedge_profit_mean"] = sabr_hedge_profit_mean_arr

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

    save_error_plot(
        result_table,
        "black_price_error",
        "sabr_price_error",
        price_error_figure,
        "Monte Carlo pricing error",
        "absolute price error",
    )

    save_error_plot(
        result_table,
        "black_hedge_error",
        "sabr_hedge_error",
        hedge_error_figure,
        "Monte Carlo hedge error",
        "absolute hedge error",
    )

    print(
        result_table.head()
    )

    print(
        "saved to",
        output_file,
    )

    print(
        "saved figure to",
        price_error_figure,
    )

    print(
        "saved figure to",
        hedge_error_figure,
    )


if __name__ == "__main__":

    main()