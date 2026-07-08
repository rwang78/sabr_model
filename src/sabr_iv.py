import numpy as np


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
    routine use
        compute Hagan SABR implied volatility

    inputs
        f: scalar, forward price
        k: scalar, strike price
        t: scalar, time to expiration
        alpha: scalar, SABR volatility level
        beta: scalar, SABR elasticity parameter
        rho: scalar, SABR correlation
        nu: scalar, SABR volatility of volatility

    returns
        sigma: scalar, SABR implied volatility
    '''

    if abs(f - k) < 1e-8:

        sigma = sabr_iv_atm(
            f,
            t,
            alpha,
            beta,
            rho,
            nu,
        )

        return sigma

    one_minus_beta = 1.0 - beta

    log_fk = np.log(f/k)

    fk_beta = (f*k)**(0.5*one_minus_beta)

    denom_correction = (
        1.0
        + (one_minus_beta**2/24.0)*(log_fk**2)
        + (one_minus_beta**4/1920.0)*(log_fk**4)
    )

    denom = fk_beta*denom_correction

    z = (nu/alpha)*fk_beta*log_fk

    inside_sqrt = 1.0 - 2.0*rho*z + z*z

    if inside_sqrt <= 0.0:

        return np.nan

    numerator = (
        np.sqrt(inside_sqrt)
        + z
        - rho
    )

    denominator = 1.0 - rho

    if numerator <= 0.0:

        return np.nan

    if denominator <= 0.0:

        return np.nan

    x_z = np.log(
        numerator/denominator
    )

    if abs(x_z) < 1e-12:

        z_over_x = 1.0

    else:

        z_over_x = z/x_z

    term_1 = (
        (one_minus_beta**2/24.0)
        *(alpha**2)
        /((f*k)**one_minus_beta)
    )

    term_2 = (
        0.25
        *rho
        *beta
        *nu
        *alpha
        /fk_beta
    )

    term_3 = (
        (2.0 - 3.0*rho*rho)
        /24.0
        *nu*nu
    )

    time_correction = 1.0 + (
        term_1
        + term_2
        + term_3
    )*t

    sigma = (
        (alpha/denom)
        *z_over_x
        *time_correction
    )

    return sigma


def sabr_iv_atm(
    f,
    t,
    alpha,
    beta,
    rho,
    nu,
):
    '''
    routine use
        compute Hagan SABR ATM implied volatility

    inputs
        f: scalar, forward price
        t: scalar, time to expiration
        alpha: scalar, SABR volatility level
        beta: scalar, SABR elasticity parameter
        rho: scalar, SABR correlation
        nu: scalar, SABR volatility of volatility

    returns
        sigma: scalar, ATM SABR implied volatility
    '''

    one_minus_beta = 1.0 - beta

    f_beta = f**one_minus_beta

    term_1 = (
        (one_minus_beta**2/24.0)
        *(alpha**2)
        /(f**(2.0 - 2.0*beta))
    )

    term_2 = (
        0.25
        *rho
        *beta
        *nu
        *alpha
        /f_beta
    )

    term_3 = (
        (2.0 - 3.0*rho*rho)
        /24.0
        *nu*nu
    )

    time_correction = 1.0 + (
        term_1
        + term_2
        + term_3
    )*t

    sigma = (
        alpha/f_beta
    )*time_correction

    return sigma