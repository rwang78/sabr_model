import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ticker = "SPY"

expiry = "2026-08-21"

input_file = (
    "results/tables/"
    "SPY_2026-08-21_hedge_output.csv"
)

output_file = (
    "results/figures/"
    "SPY_2026-08-21_call_price.png"
)


def main():
    '''
    routine use
        compare market call prices with
        Black and SABR model prices

    inputs
        none

    returns
        none
    '''

    hedge_table = pd.read_csv(
        input_file,
    )

    strike_arr = hedge_table[
        "strike"
    ].values

    market_call_arr = hedge_table[
        "mid"
    ].values

    black_call_arr = hedge_table[
        "black_call"
    ].values

    black_mc_call_arr = hedge_table[
        "black_mc_call"
    ].values

    sabr_call_arr = hedge_table[
        "sabr_call"
    ].values

    sabr_mc_call_arr = hedge_table[
        "sabr_mc_call"
    ].values

    black_rmse = np.sqrt(
        np.mean(
            (
                black_call_arr
                - market_call_arr
            )**2
        )
    )

    black_mc_rmse = np.sqrt(
        np.mean(
            (
                black_mc_call_arr
                - market_call_arr
            )**2
        )
    )

    sabr_rmse = np.sqrt(
        np.mean(
            (
                sabr_call_arr
                - market_call_arr
            )**2
        )
    )

    sabr_mc_rmse = np.sqrt(
        np.mean(
            (
                sabr_mc_call_arr
                - market_call_arr
            )**2
        )
    )

    black_mae = np.mean(
        np.abs(
            black_call_arr
            - market_call_arr
        )
    )

    black_mc_mae = np.mean(
        np.abs(
            black_mc_call_arr
            - market_call_arr
        )
    )

    sabr_mae = np.mean(
        np.abs(
            sabr_call_arr
            - market_call_arr
        )
    )

    sabr_mc_mae = np.mean(
        np.abs(
            sabr_mc_call_arr
            - market_call_arr
        )
    )

    print()

    print(
        "pricing errors against market"
    )

    print(
        f"black closed form rmse : {black_rmse:.6f}"
    )

    print(
        f"black monte carlo rmse : {black_mc_rmse:.6f}"
    )

    print(
        f"sabr hagan rmse        : {sabr_rmse:.6f}"
    )

    print(
        f"sabr monte carlo rmse  : {sabr_mc_rmse:.6f}"
    )

    print()

    print(
        f"black closed form mae  : {black_mae:.6f}"
    )

    print(
        f"black monte carlo mae  : {black_mc_mae:.6f}"
    )

    print(
        f"sabr hagan mae         : {sabr_mae:.6f}"
    )

    print(
        f"sabr monte carlo mae   : {sabr_mc_mae:.6f}"
    )

    plt.figure(
        figsize=(8, 5),
    )

    plt.plot(
        strike_arr,
        market_call_arr,
        color="black",
        linewidth=2,
        label="market",
    )

    plt.plot(
        strike_arr,
        black_call_arr,
        color="blue",
        linewidth=2,
        label="black closed form",
    )

    plt.plot(
        strike_arr,
        black_mc_call_arr,
        color="blue",
        linestyle="--",
        linewidth=2,
        label="black monte carlo",
    )

    plt.plot(
        strike_arr,
        sabr_call_arr,
        color="orange",
        linewidth=2,
        label="sabr hagan",
    )

    plt.plot(
        strike_arr,
        sabr_mc_call_arr,
        color="orange",
        linestyle="--",
        linewidth=2,
        label="sabr monte carlo",
    )

    plt.xlabel(
        "strike",
    )

    plt.ylabel(
        "call price",
    )

    plt.title(
        (
            ticker
            + " "
            + expiry
            + " call price comparison"
        ),
    )

    plt.grid(
        True,
    )

    plt.legend()

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight",
    )

    plt.show()


if __name__ == "__main__":

    main()

'''
pricing errors against market
black closed form rmse : 1.937651
black monte carlo rmse : 4.963974
sabr hagan rmse        : 0.339667
sabr monte carlo rmse  : 6.201467

black closed form mae  : 1.604073
black monte carlo mae  : 4.651962
sabr hagan mae         : 0.243707
sabr monte carlo mae   : 4.908722
'''