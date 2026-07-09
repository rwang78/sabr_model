import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_forward_path_arr(
    forward_path_arr,
    t,
    model_name,
):
    '''
    routine use
        plot monte carlo forward price paths and save plot and csv

    inputs
        forward_path_arr: 2d array (n_paths, n_steps + 1), simulated forward paths
        t: scalar, time to expiration
        model_name: string, model name

    returns
        none
    '''

    n_paths = forward_path_arr.shape[0]
    n_steps = forward_path_arr.shape[1] - 1

    time_arr = np.linspace(
        0.0,
        t,
        n_steps + 1,
    )

    for i in range(n_paths):

        plt.plot(
            time_arr,
            forward_path_arr[i],
        )

    plt.xlabel("time")
    plt.ylabel("forward price")
    plt.title(
        model_name
        + " monte carlo forward paths"
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
        + model_name
        + "_forward_paths.png"
    )

    csv_file = (
        "results/tables/"
        + "forward_paths_"
        + model_name
        + ".csv"
    )

    plt.savefig(
        figure_file,
        dpi=300,
        bbox_inches="tight",
    )

    plt.show()

    plt.close()

    table = pd.DataFrame(
        forward_path_arr.T,
    )

    table.columns = [
        f"path_{i}"
        for i in range(n_paths)
    ]

    table.insert(
        0,
        "time",
        time_arr,
    )

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