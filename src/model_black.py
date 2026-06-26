'''
routines to compute Black option prices using forward price

pricing
    European call
    European put

greeks
    forward delta
    vega
    volga
    vanna

notes
    uses forward price f and discount factor df

adapted from "7_Complete_Black_Scholes_Real_Markets.ipynb"
where we use forward price instead of spot price 

'''

import numpy as np
from scipy.stats import norm


def black_d1(f, k, sigma, t):
    '''
    compute d1 in the Black forward formula

    inputs
        f: scalar, forward price
        k: scalar, strike price
        sigma: scalar, volatility
        t: scalar, time to expiration

    returns
        d1: scalar
    '''

    numerator = np.log(f/k) + 0.5*sigma**2*t
    denominator = sigma*np.sqrt(t)

    d1 = numerator/denominator

    return d1


def black_d2(f, k, sigma, t):
    '''
    routine:
        compute d2 in the Black forward formula

    inputs
        f: scalar, forward price
        k: scalar, strike price
        sigma: scalar, volatility
        t: scalar, time to expiration

    returns
        d2: scalar
    '''

    d1 = black_d1(f, k, sigma, t)

    d2 = d1 - sigma*np.sqrt(t)

    return d2


def black_call(f, k, sigma, t, df):
    '''
    routine:
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

    d1 = black_d1(f, k, sigma, t)
    d2 = black_d2(f, k, sigma, t)

    call = df*(f*norm.cdf(d1) - k*norm.cdf(d2))

    return call


def black_put(f, k, sigma, t, df):
    '''
    routine:
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

    call = black_call(f, k, sigma, t, df)

    put = call + df*(k - f)

    return put


def black_call_delta(f, k, sigma, t, df):
    '''
    routine:
        compute call delta with respect to forward price

    inputs
        f: scalar, forward price
        k: scalar, strike price
        sigma: scalar, volatility
        t: scalar, time to expiration
        df: scalar, discount factor

    returns
        delta: scalar, forward delta of European call
    '''

    d1 = black_d1(f, k, sigma, t)

    delta = df*norm.cdf(d1)

    return delta


def black_put_delta(f, k, sigma, t, df):
    '''
    routine:
        compute put delta with respect to forward price

    inputs
        f: scalar, forward price
        k: scalar, strike price
        sigma: scalar, volatility
        t: scalar, time to expiration
        df: scalar, discount factor

    returns
        delta: scalar, forward delta of European put
    '''

    d1 = black_d1(f, k, sigma, t)

    delta = df*(norm.cdf(d1) - 1.0)

    return delta


def black_vega(f, k, sigma, t, df):
    '''
    routine:
        compute vega using forward price

    inputs
        f: scalar, forward price
        k: scalar, strike price
        sigma: scalar, volatility
        t: scalar, time to expiration
        df: scalar, discount factor

    returns
        vega: scalar, vega of European call and put
    '''

    d1 = black_d1(f, k, sigma, t)

    vega = df*f*np.sqrt(t)*norm.pdf(d1)

    return vega


def black_volga(f, k, sigma, t, df):
    '''
    routine:
        compute volga using forward price

    inputs
        f: scalar, forward price
        k: scalar, strike price
        sigma: scalar, volatility
        t: scalar, time to expiration
        df: scalar, discount factor

    returns
        volga: scalar, volga of European call and put
    '''

    d1 = black_d1(f, k, sigma, t)
    d2 = black_d2(f, k, sigma, t)

    vega = black_vega(f, k, sigma, t, df)

    volga = vega*d1*d2/sigma

    return volga


def black_vanna(f, k, sigma, t, df):
    '''
    routine:
        compute vanna using forward price

    inputs
        f: scalar, forward price
        k: scalar, strike price
        sigma: scalar, volatility
        t: scalar, time to expiration
        df: scalar, discount factor

    returns
        vanna: scalar, vanna of European call and put
    '''

    d1 = black_d1(f, k, sigma, t)
    d2 = black_d2(f, k, sigma, t)

    vanna = -df*norm.pdf(d1)*d2/sigma

    return vanna