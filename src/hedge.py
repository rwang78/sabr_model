import numpy as np

from src.black_call_put_close import black_call


def black_hedge(
    f,
    k,
    sigma,
    t,
    df,
    path_arr,
    delta_arr,
):
    '''
    routine use
        compute pathwise call payoff, hedge profit,
        hedge value, hedge error, monte carlo price, and price error
        under Black forward dynamics

    inputs
        f: scalar, initial forward price
        k: scalar, strike price
        sigma: scalar, Black volatility
        t: scalar, time to expiration
        df: scalar, discount factor
        path_arr: 2d array (n_paths, n_steps + 1), simulated forward price paths
        delta_arr: 2d array (n_paths, n_steps), forward hedge ratios

    returns
        hedge_value_arr: 1d array (n_paths), pathwise hedge values
        call_payout_arr: 1d array (n_paths), pathwise discounted call payoffs
        hedge_profit_arr: 1d array (n_paths), pathwise hedge profits
        hedge_value_mean: scalar, mean hedge value
        call_price: scalar, Black closed form call price
        hedge_error: scalar, absolute hedge error
        mc_call_price: scalar, monte carlo call price
        price_error: scalar, absolute monte carlo pricing error
    '''

    n_steps = path_arr.shape[1] - 1

    call_payout_arr = df*np.maximum(
        path_arr[:, -1] - k,
        0.0,
    )

    hedge_profit_arr = df*np.sum(
        (
            path_arr[:, 1:n_steps + 1]
            - path_arr[:, 0:n_steps]
        )*delta_arr,
        axis=1,
    )

    hedge_value_arr = (
        call_payout_arr
        - hedge_profit_arr
    )

    hedge_value_mean = np.mean(
        hedge_value_arr,
    )

    call_price = black_call(
        f,
        k,
        sigma,
        t,
        df,
    )

    hedge_error = abs(
        hedge_value_mean
        - call_price
    )

    mc_call_price = np.mean(
        call_payout_arr,
    )

    price_error = abs(
        mc_call_price
        - call_price
    )

    return (
        hedge_value_arr,
        call_payout_arr,
        hedge_profit_arr,
        hedge_value_mean,
        call_price,
        hedge_error,
        mc_call_price,
        price_error,
    )