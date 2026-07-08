import numpy as np 

from src.sabr_iv import(
    sabr_iv,
    sabr_iv_atm
)

from src.black_call_put_close import(
    black_call
)

from src.black_greeks import(
    black_call_delta, 
    black_put_delta, 
    black_vega
)

def sabr_delta_fd(
    f,
    k,
    t,
    df,
    alpha,
    beta,
    rho,
    nu,
    bump=1e-4,
):
    '''
    routine use
        compute SABR delta using eq (27)

    inputs
        f: scalar, forward price
        k: scalar, strike price
        t: scalar, time to expiration
        df: scalar, discount factor
        alpha: scalar, volatility level
        beta: scalar, elasticity parameter
        rho: scalar, correlation
        nu: scalar, volatility of volatility
        bump: scalar, finite difference bump for forward

    returns
        delta: scalar, SABR delta
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

    if np.isnan(sigma):
        return np.nan

    bs_delta = black_call_delta(
        f,
        k,
        sigma,
        t,
        df,
    )

    bs_vega_value = black_vega(
        f,
        k,
        sigma,
        t,
        df,
    )

    f_up = f + bump
    f_down = f - bump

    if f_down <= 0.0:
        return np.nan

    sigma_up = sabr_iv(
        f_up,
        k,
        t,
        alpha,
        beta,
        rho,
        nu,
    )

    sigma_down = sabr_iv(
        f_down,
        k,
        t,
        alpha,
        beta,
        rho,
        nu,
    )

    if np.isnan(sigma_up):
        return np.nan

    if np.isnan(sigma_down):
        return np.nan

    dsigma_df = (sigma_up - sigma_down)/(2.0*bump)

    delta = bs_delta + bs_vega_value*dsigma_df

    return delta

