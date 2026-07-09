'''
routines to compute Black implied volatility

the implied volatility is obtained by solving

    Black forward price(volatility) = market price

using a one dimensional root finding algorithm.

the solver is supplied as an input, allowing different
methods such as brent, bisection, newton, or secant
to be used without modifying the implied volatility routine.
'''

import numpy as np
from scipy.optimize import brentq

from src.black_call_put_close import black_call


def call_price_error(
    sigma,
    price,
    f,
    k,
    t,
    df,
):
    '''
    routine use
        compute call pricing error

    inputs
        sigma: scalar, volatility
        price: scalar, market price
        f: scalar, forward price
        k: scalar, strike price
        t: scalar, time to expiration
        df: scalar, discount factor

    returns
        error: scalar
    '''

    model_price = black_call(
        f,
        k,
        sigma,
        t,
        df,
    )

    error = model_price - price

    return error


def black_call_iv(
    price,
    f,
    k,
    t,
    df,
    solver,
):
    '''
    routine use
        compute Black implied volatility

    inputs
        price: scalar, market call price
        f: scalar, forward price
        k: scalar, strike price
        t: scalar, time to expiration
        df: scalar, discount factor
        solver: root finding routine

    returns
        sigma: scalar, implied volatility
    '''

    intrinsic_value = f - k

    if intrinsic_value < 0.0:

        intrinsic_value = 0.0

    intrinsic_value = df*intrinsic_value

    if price <= intrinsic_value:

        return np.nan

    sigma_low = 1e-6
    sigma_high = 5.0

    error_low = call_price_error(
        sigma_low,
        price,
        f,
        k,
        t,
        df,
    )

    error_high = call_price_error(
        sigma_high,
        price,
        f,
        k,
        t,
        df,
    )

    if error_low*error_high > 0.0:

        return np.nan

    sigma = solver(
        call_price_error,
        sigma_low,
        sigma_high,
        price,
        f,
        k,
        t,
        df,
    )

    return sigma


def brent_solver(
    func,
    x_low,
    x_high,
    *args,
):
    '''
    routine use
        solve f(x)=0 using Brent's method

    inputs
        func: function
        x_low: scalar
        x_high: scalar
        args: additional arguments

    returns
        root: scalar
    '''

    root = brentq(
        func,
        x_low,
        x_high,
        args=args,
    )

    return root