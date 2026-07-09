import numpy as np
import matplotlib.pyplot as plt


def plot_hedge_value_histogram(
    black_hedge_value_arr,
    sabr_hedge_value_arr,
    black_call_price,
    sabr_call_price,
    output_file=None,
):
    '''
    routine use
        plot histogram of Black and SABR hedged values

    inputs
        black_hedge_value_arr: 1d array (n_paths), Black hedged values
        sabr_hedge_value_arr: 1d array (n_paths), SABR hedged values
        black_call_price: scalar, closed form Black call price
        sabr_call_price: scalar, SABR call price from Hagan implied volatility
        output_file: string or none, output figure path

    returns
        none
    '''

    black_mean = np.mean(
        black_hedge_value_arr
    )

    sabr_mean = np.mean(
        sabr_hedge_value_arr
    )

    plt.figure(
        figsize=(
            8,
            8,
        )
    )

    plt.hist(
        black_hedge_value_arr,
        bins=50,
        density=True,
        alpha=0.5,
        label="black hedged values",
    )

    plt.hist(
        sabr_hedge_value_arr,
        bins=50,
        density=True,
        alpha=0.5,
        label="sabr hedged values",
    )

    plt.axvline(
        black_mean,
        label=f"black mean hedge value: {black_mean:.4f}",
        linestyle="--",
        linewidth=3,
    )

    plt.axvline(
        sabr_mean,
        label=f"sabr mean hedge value: {sabr_mean:.4f}",
        linestyle="--",
        linewidth=3,
    )

    plt.axvline(
        black_call_price,
        label=f"black closed form call: {black_call_price:.4f}",
        linewidth=3,
    )

    plt.axvline(
        sabr_call_price,
        label=f"sabr hagan call: {sabr_call_price:.4f}",
        linewidth=3,
    )

    plt.xlabel(
        "hedged value"
    )

    plt.ylabel(
        "density"
    )

    plt.title(
        "histogram of black and sabr hedged values"
    )

    plt.legend()

    if output_file is not None:

        plt.savefig(
            output_file,
            bbox_inches="tight",
        )

    plt.show()