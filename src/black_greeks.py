import numpy as np
from scipy.stats import norm

from src.black_call_put_close import (
    black_d1,
    black_d2,
)


def black_call_delta(
    f,
    k,
    sigma,
    t,
    df,
):
    '''
    routine use
        compute Black call delta with respect to forward price

    inputs
        f: scalar, forward price
        k: scalar, strike price
        sigma: scalar, volatility
        t: scalar, time to expiration
        df: scalar, discount factor

    returns
        delta: scalar, forward delta of European call
    '''

    d1 = black_d1(
        f,
        k,
        sigma,
        t,
    )

    delta = df*norm.cdf(
        d1
    )

    return delta


def black_put_delta(
    f,
    k,
    sigma,
    t,
    df,
):
    '''
    routine use
        compute Black put delta with respect to forward price

    inputs
        f: scalar, forward price
        k: scalar, strike price
        sigma: scalar, volatility
        t: scalar, time to expiration
        df: scalar, discount factor

    returns
        delta: scalar, forward delta of European put
    '''

    d1 = black_d1(
        f,
        k,
        sigma,
        t,
    )

    delta = df*(
        norm.cdf(
            d1
        )
        - 1.0
    )

    return delta


def black_vega(
    f,
    k,
    sigma,
    t,
    df,
):
    '''
    routine use
        compute Black vega using forward price

    inputs
        f: scalar, forward price
        k: scalar, strike price
        sigma: scalar, volatility
        t: scalar, time to expiration
        df: scalar, discount factor

    returns
        vega: scalar, vega of European call and put
    '''

    d1 = black_d1(
        f,
        k,
        sigma,
        t,
    )

    vega = df*f*np.sqrt(
        t
    )*norm.pdf(
        d1
    )

    return vega


def black_gamma(
    f,
    k,
    sigma,
    t,
    df,
):
    '''
    routine use
        compute Black gamma with respect to forward price

    inputs
        f: scalar, forward price
        k: scalar, strike price
        sigma: scalar, volatility
        t: scalar, time to expiration
        df: scalar, discount factor

    returns
        gamma: scalar, forward gamma of European call and put
    '''

    d1 = black_d1(
        f,
        k,
        sigma,
        t,
    )

    gamma = df*norm.pdf(
        d1
    )/(
        f*sigma*np.sqrt(
            t
        )
    )

    return gamma


def black_volga(
    f,
    k,
    sigma,
    t,
    df,
):
    '''
    routine use
        compute Black volga using forward price

    inputs
        f: scalar, forward price
        k: scalar, strike price
        sigma: scalar, volatility
        t: scalar, time to expiration
        df: scalar, discount factor

    returns
        volga: scalar, volga of European call and put
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

    vega = black_vega(
        f,
        k,
        sigma,
        t,
        df,
    )

    volga = vega*d1*d2/sigma

    return volga


def black_vanna(
    f,
    k,
    sigma,
    t,
    df,
):
    '''
    routine use
        compute Black vanna using forward price

    inputs
        f: scalar, forward price
        k: scalar, strike price
        sigma: scalar, volatility
        t: scalar, time to expiration
        df: scalar, discount factor

    returns
        vanna: scalar, vanna of European call and put
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

    vanna = -df*norm.pdf(
        d1
    )*d2/sigma

    return vanna