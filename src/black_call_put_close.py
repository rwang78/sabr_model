'''
routines to compute Black option prices using forward price

pricing
    European call
    European put

notes
    uses forward price f and discount factor df
'''

import numpy as np
from scipy.stats import norm


def black_d1(
    f,
    k,
    sigma,
    t,
):
    '''
    routine use
        compute d1 in the Black forward formula

    inputs
        f: scalar, forward price
        k: scalar, strike price
        sigma: scalar, volatility
        t: scalar, time to expiration

    returns
        d1: scalar
    '''

    numerator = (
        np.log(
            f/k
        )
        + 0.5*sigma*sigma*t
    )

    denominator = sigma*np.sqrt(
        t
    )

    d1 = numerator/denominator

    return d1


def black_d2(
    f,
    k,
    sigma,
    t,
):
    '''
    routine use
        compute d2 in the Black forward formula

    inputs
        f: scalar, forward price
        k: scalar, strike price
        sigma: scalar, volatility
        t: scalar, time to expiration

    returns
        d2: scalar
    '''

    d1 = black_d1(
        f,
        k,
        sigma,
        t,
    )

    d2 = d1 - sigma*np.sqrt(
        t
    )

    return d2


def black_call(
    f,
    k,
    sigma,
    t,
    df,
):
    '''
    routine use
        compute European call price using forward price

    inputs
        f: scalar, forward price
        k: scalar, strike price
        sigma: scalar, volatility
        t: scalar, time to expiration
        df: scalar, discount factor

    returns
        call: scalar, European call price
    '''

    d1 = black_d1(
        f,
        k,
        sigma,
        t,
    )

    d2 = black_d2(
        f,
        k,
        sigma,
        t,
    )

    call = df*(
        f*norm.cdf(
            d1
        )
        - k*norm.cdf(
            d2
        )
    )

    return call


def black_put(
    f,
    k,
    sigma,
    t,
    df,
):
    '''
    routine use
        compute European put price using forward price

    inputs
        f: scalar, forward price
        k: scalar, strike price
        sigma: scalar, volatility
        t: scalar, time to expiration
        df: scalar, discount factor

    returns
        put: scalar, European put price
    '''

    d1 = black_d1(
        f,
        k,
        sigma,
        t,
    )

    d2 = black_d2(
        f,
        k,
        sigma,
        t,
    )

    put = df*(
        k*norm.cdf(
            -d2
        )
        - f*norm.cdf(
            -d1
        )
    )

    return put