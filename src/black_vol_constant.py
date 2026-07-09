import numpy as np


def black_constant_vol(
    price_arr,
    trading_days=252,
):
    '''
    routine use
        compute constant Black volatility from historical log returns

    inputs
        price_arr: 1d array (n), historical underlying prices
        trading_days: scalar, number of trading days per year

    returns
        sigma: scalar, annualized historical volatility
    '''

    n = len(
        price_arr
    )

    log_return_arr = np.zeros(
        n - 1
    )

    for i in range(n - 1):

        log_return_arr[i] = np.log(
            price_arr[i + 1]
            / price_arr[i]
        )

    daily_sigma = np.std(
        log_return_arr,
        ddof=1,
    )

    sigma = daily_sigma*np.sqrt(
        trading_days
    )

    return sigma