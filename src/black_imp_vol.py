
'''
routines to compute black implied volatility \sigma_market later to use in calibr.py

The implied volatility is obtained by solving

    black price(volatility) = market price

using a one dimensional root finding algomarket_ivrithm.

The solver is supplied as an input, allowing different
methods such as brent, bisection, newton, or secant
to be used without modifying the implied volatility
routine.
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

    #computes \max(f-k,0) and discounts it to today df*\max(f-k,0)

    diff = f - k

    if diff < 0.0:
        diff = 0.0

    diff = df*diff

    # if mkt price satisfies C_{\mathrm{market}}\le df\max(f-k,0), no positive implied volatility exists
    if price <= diff:
        return np.nan

    # choose a search interval
    # The upper bound corresponds to roughly 500% annual volatility, which is far beyond normal market values but ensures the root is almost always enclosed.
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

    # verify a sign change 
    if error_low*error_high > 0.0:
        return np.nan

    # solve the root finding problem 
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

# some solvers we can use 
def brent_solver(
    func,
    x_low,
    x_high,
    *args,
):
    '''
    solve f(x)=0 using Brent's method

    inputs
        func: function
        x_low: scalar
        x_high: scalar
        args: additional arguments

    returns
        root: scalar

    Brent, R. P. (1973), "Chapter 4: An Algorithm with Guaranteed Convergence for Finding a Zero of a Function", Algorithms for Minimization without Derivatives, Englewood Cliffs, NJ: Prentice-Hall, ISBN 0-13-022335-2
    brent is preferred: https://www.quantlib.org/slides/dima-ql-intro-2.pdf?utm_source
    '''

    root = brentq(
        func,
        x_low,
        x_high,
        args=args,
    )

    return root

'''
it is also possible to implement newton's method, midpoint method, or other equations solver 
'''