import numpy as np

from src.model_black import black_call


def sabr_iv(
    f,
    k,
    t,
    alpha,
    beta,
    rho,
    nu,
):
    '''
    compute Hagan SABR implied volatility
    eq (17a)

    inputs
        f: scalar, forward price
        k: scalar, strike price
        t: scalar, time to expiration
        alpha: scalar, volatility level
        beta: scalar, elasticity parameter
        rho: scalar, correlation
        nu: scalar, volatility of volatility

    returns
        sigma: scalar, SABR implied volatility
    '''

    pass


def sabr_call_price(
    f,
    k,
    t,
    alpha,
    beta,
    rho,
    nu,
    #df=1.0,
    df
):
    '''
    compute SABR call price using Hagan volatility and Black price

    inputs
        f: scalar, forward price
        k: scalar, strike price
        t: scalar, time to expiration
        alpha: scalar, volatility level
        beta: scalar, elasticity parameter
        rho: scalar, correlation
        nu: scalar, volatility of volatility
        df: scalar, discount factor

    returns
        price: scalar, SABR call price
    '''

    sigma = sabr_iv(
        f,
        k,
        t,
        alpha,
        beta,
        rho,
        nu,
    )

    price = black_call(
        f,
        k,
        sigma,
        t,
        df,
    )

    return price


def sabr_delta_fd(
    f,
    k,
    t,
    alpha,
    beta,
    rho,
    nu,
    #df=1.0,
    #bump=0.01,
    df, 
    bump, 
):
    '''
    compute SABR call delta by central finite difference

    inputs
        f: scalar, forward price
        k: scalar, strike price
        t: scalar, time to expiration
        alpha: scalar, volatility level
        beta: scalar, elasticity parameter
        rho: scalar, correlation
        nu: scalar, volatility of volatility
        df: scalar, discount factor
        bump: scalar, finite difference bump size

    returns
        delta: scalar, finite difference call delta
    '''
    
    pass




# 