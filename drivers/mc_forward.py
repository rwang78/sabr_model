import os
import numpy as np
import pandas as pd

from src.mc_forward_black import black_forward_path_arr
from src.mc_forward_sabr import simulate_sabr_euler_maruyama
from src.plot_forward import plot_forward_path_arr


ticker = "SPY"

expiry = "2026-08-21"

input_file = (
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

n_paths = 1000
n_steps = 100
n_save_paths = n_paths
n_plot_paths = 50
seed = 0


def save_forward_paths(
    path_file,
    model,
    forward_path_arr,
    t,
    alpha_path_arr=None,
):
    '''
    routine use
        save selected Monte Carlo forward paths to csv

    inputs
        path_file: string, output csv file
        model: string, model name
        forward_path_arr: 2d array (n_paths, n_steps + 1), forward price paths
        t: scalar, time to expiration
        alpha_path_arr: 2d array (n_paths, n_steps + 1), SABR alpha paths or none

    returns
        none
    '''

    n_paths_local = forward_path_arr.shape[0]
    n_steps_local = forward_path_arr.shape[1] - 1

    n_save = min(
        n_save_paths,
        n_paths_local,
    )

    time_arr = np.linspace(
        0.0,
        t,
        n_steps_local + 1,
    )

    row_list = []

    for i in range(n_save):

        for j in range(n_steps_local + 1):

            row = {
                "model": model,
                "path_id": i,
                "step": j,
                "time": time_arr[j],
                "forward": forward_path_arr[i, j],
            }

            if alpha_path_arr is not None:

                row["alpha"] = alpha_path_arr[i, j]

            row_list.append(
                row
            )

    path_table = pd.DataFrame(
        row_list
    )

    output_dir = os.path.dirname(
        path_file,
    )

    if output_dir != "":

        os.makedirs(
            output_dir,
            exist_ok=True,
        )

    path_table.to_csv(
        path_file,
        index=False,
    )


def main():
    '''
    routine use
        generate Black and SABR Monte Carlo forward paths from hedge output table

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
            "black_constant_vol",
            "sabr_alpha",
            "sabr_beta",
            "sabr_rho",
            "sabr_nu",
        ]
    )


    # the spot price and all constants are the same 
    row = valid_table.iloc[
    0
    ]

    f = row["spot"]

    black_sigma = row["black_constant_vol"]

    alpha = row["sabr_alpha"]
    beta = row["sabr_beta"]
    rho = row["sabr_rho"]
    nu = row["sabr_nu"]




    black_path_arr = black_forward_path_arr(
        f,
        black_sigma,
        t,
        n_paths,
        n_steps,
        seed,
    )

    save_forward_paths(
        black_path_file,
        "black",
        black_path_arr,
        t,
    )

    plot_forward_path_arr(
        black_path_arr[
            0:n_plot_paths,
            :,
        ],
        t,
        "mc_forward_black_SPY_2026-08-21",
    )

    F, alpha_path = simulate_sabr_euler_maruyama(
        f,
        alpha,
        beta,
        rho,
        nu,
        t,
        n_steps,
        n_paths,
        seed,
    )

    sabr_path_arr = F.T
    sabr_alpha_path_arr = alpha_path.T

    save_forward_paths(
        sabr_path_file,
        "sabr",
        sabr_path_arr,
        t,
        sabr_alpha_path_arr,
    )

    plot_forward_path_arr(
        sabr_path_arr[
            0:n_plot_paths,
            :,
        ],
        t,
        "mc_forward_sabr_SPY_2026-08-21",
    )

    print(
        "black path shape:",
        black_path_arr.shape,
    )

    print(
        "sabr path shape:",
        sabr_path_arr.shape,
    )

    print(
        "saved to",
        black_path_file,
    )

    print(
        "saved to",
        sabr_path_file,
    )


if __name__ == "__main__":

    main()