from src.sabr_iv import(
    sabr_iv,
    sabr_iv_atm
)

from src.black_call_put_close import(
    black_call
)


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


