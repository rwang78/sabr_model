import numpy as np
import pandas as pd

from src.model_sabr import sabr_iv


def monte_carlo_call(
    f,
    k,
    sigma,
    t,
    df,
    n_paths,
):
    '''
    compute call price by monte carlo under forward dynamics

    inputs
        f: scalar, forward price
        k: scalar, strike price
        sigma: scalar, volatility
        t: scalar, time to expiration
        df: scalar, discount factor
        n_paths: integer, number of monte carlo paths

    returns
        price: scalar, monte carlo call price
    '''

    payoff_sum = 0.0

    for i in range(n_paths):

        z = np.random.normal()

        terminal_forward = f*np.exp(
            -0.5*sigma**2*t
            + sigma*np.sqrt(t)*z
        )

        payoff = terminal_forward - k

        if payoff < 0.0:
            payoff = 0.0

        payoff_sum += payoff

    price = df*payoff_sum/n_paths

    return price


def pricing_table(
    iv_table,
    f,
    t,
    sabr_params,
    df,
    n_paths,
    seed,
):
    '''
    build monte carlo pricing comparison table

    inputs
        iv_table: dataframe, market option data
        f: scalar, forward price
        t: scalar, time to expiration
        sabr_params: dictionary, calibrated SABR parameters
        df: scalar, discount factor
        n_paths: integer, number of monte carlo paths
        seed: integer, random seed

    returns
        table: dataframe, pricing comparison table
    '''

    np.random.seed(seed)

    strikes = []
    market_iv = []

    for i in range(len(iv_table)):

        row = iv_table.iloc[i]

        strikes.append(row['strike'])
        market_iv.append(row['market_iv'])

    atm_index = 0
    atm_error = abs(strikes[0] - f)

    for i in range(len(strikes)):

        error = abs(strikes[i] - f)

        if error < atm_error:

            atm_error = error
            atm_index = i

    bs_iv = market_iv[atm_index]

    rows = []

    for i in range(len(iv_table)):

        row = iv_table.iloc[i]

        k = row['strike']
        market_price = row['market_price']

        bs_price = monte_carlo_call(
            f,
            k,
            bs_iv,
            t,
            df,
            n_paths,
        )

        sabr_vol = sabr_iv(
            f,
            k,
            t,
            sabr_params['alpha'],
            sabr_params['beta'],
            sabr_params['rho'],
            sabr_params['nu'],
        )

        sabr_price = monte_carlo_call(
            f,
            k,
            sabr_vol,
            t,
            df,
            n_paths,
        )

        output_row = {}

        output_row['strike'] = k
        output_row['market_price'] = market_price

        output_row['bs_price'] = bs_price
        output_row['sabr_price'] = sabr_price

        output_row['market_iv'] = row['market_iv']
        output_row['bs_iv'] = bs_iv
        output_row['sabr_iv'] = sabr_vol

        output_row['bs_price_error'] = bs_price - market_price
        output_row['sabr_price_error'] = sabr_price - market_price

        rows.append(output_row)

    table = pd.DataFrame(rows)

    return table