import numpy as np
import pandas as pd

from src.model_black import (
    black_call,
    black_call_delta,
)

from src.model_sabr import (
    sabr_call_price,
    sabr_delta_fd,
)


def gbm_paths(
    s0,
    sigma,
    t,
    r,
    n_paths,
    n_steps,
    seed,
):
    '''
    simulate gbm paths

    inputs
        s0: scalar, initial spot price
        sigma: scalar, volatility
        t: scalar, time to expiration
        r: scalar, risk free rate
        n_paths: integer, number of monte carlo paths
        n_steps: integer, number of time steps
        seed: integer, random seed

    returns
        paths: 2d array, simulated stock paths
    '''

    np.random.seed(seed)

    dt = t/n_steps

    paths = np.zeros(
        (n_paths, n_steps + 1)
    )

    for i in range(n_paths):

        paths[i, 0] = s0

        for j in range(1, n_steps + 1):

            z = np.random.normal()

            drift = (
                r
                - 0.5*sigma**2
            )

            drift = drift*dt

            diffusion = (
                sigma
                * np.sqrt(dt)
                * z
            )

            paths[i, j] = paths[i, j - 1]*np.exp(
                drift
                + diffusion
            )

    return paths


def call_payoff(
    spot,
    k,
):
    '''
    compute call payoff

    inputs
        spot: scalar, final spot price
        k: scalar, strike price

    returns
        payoff: scalar
    '''

    payoff = spot - k

    if payoff < 0.0:
        payoff = 0.0

    return payoff


def hedge_one_path(
    path,
    k,
    initial_sigma,
    sabr_params,
    r,
    t,
    df,
):
    '''
    run black and sabr delta hedge on one path

    inputs
        path: 1d array, stock path
        k: scalar, strike price
        initial_sigma: scalar, black volatility
        sabr_params: dictionary, sabr parameters
        r: scalar, risk free rate
        t: scalar, time to expiration
        df: scalar, discount factor

    returns
        result: dictionary, hedge errors
    '''

    n_steps = len(path) - 1
    dt = t/n_steps

    spot = path[0]

    black_price = black_call(
        spot,
        k,
        initial_sigma,
        t,
        df,
    )

    black_delta = black_call_delta(
        spot,
        k,
        initial_sigma,
        t,
        df,
    )

    black_cash = black_price - black_delta*spot
    black_shares = black_delta

    sabr_price = sabr_call_price(
        spot,
        k,
        t,
        sabr_params['alpha'],
        sabr_params['beta'],
        sabr_params['rho'],
        sabr_params['nu'],
        df,
    )

    sabr_delta = sabr_delta_fd(
        spot,
        k,
        t,
        sabr_params['alpha'],
        sabr_params['beta'],
        sabr_params['rho'],
        sabr_params['nu'],
        df,
    )

    sabr_cash = sabr_price - sabr_delta*spot
    sabr_shares = sabr_delta

    for j in range(1, n_steps + 1):

        tau = t - j*dt

        if tau < 1e-8:
            tau = 1e-8

        spot = path[j]

        black_cash = black_cash*np.exp(r*dt)

        new_black_delta = black_call_delta(
            spot,
            k,
            initial_sigma,
            tau,
            df,
        )

        black_trade = new_black_delta - black_shares
        black_cash = black_cash - black_trade*spot
        black_shares = new_black_delta

        sabr_cash = sabr_cash*np.exp(r*dt)

        new_sabr_delta = sabr_delta_fd(
            spot,
            k,
            tau,
            sabr_params['alpha'],
            sabr_params['beta'],
            sabr_params['rho'],
            sabr_params['nu'],
            df,
        )

        sabr_trade = new_sabr_delta - sabr_shares
        sabr_cash = sabr_cash - sabr_trade*spot
        sabr_shares = new_sabr_delta

    final_spot = path[-1]

    payoff = call_payoff(
        final_spot,
        k,
    )

    black_portfolio = black_cash + black_shares*final_spot
    sabr_portfolio = sabr_cash + sabr_shares*final_spot

    result = {}

    result['black_hedging_error'] = black_portfolio - payoff
    result['sabr_hedging_error'] = sabr_portfolio - payoff
    result['payoff'] = payoff
    result['final_spot'] = final_spot

    return result


def monte_carlo_hedging(
    paths,
    strikes,
    initial_sigmas,
    sabr_params,
    r,
    t,
    df,
):
    '''
    run monte carlo hedge experiment over paths and strikes

    inputs
        paths: 2d array, stock paths
        strikes: list, strike prices
        initial_sigmas: list, initial black volatilities
        sabr_params: dictionary, sabr parameters
        r: scalar, risk free rate
        t: scalar, time to expiration
        df: scalar, discount factor

    returns
        hedge_table: dataframe, hedge errors
    '''

    rows = []

    n_paths = paths.shape[0]

    for i in range(n_paths):

        path = paths[i, :]

        for j in range(len(strikes)):

            k = strikes[j]
            initial_sigma = initial_sigmas[j]

            result = hedge_one_path(
                path,
                k,
                initial_sigma,
                sabr_params,
                r,
                t,
                df,
            )

            result['path_id'] = i
            result['strike'] = k
            result['initial_sigma'] = initial_sigma

            rows.append(result)

    hedge_table = pd.DataFrame(rows)

    return hedge_table