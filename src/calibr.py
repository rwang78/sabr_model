'''
routines for sabr parameter calibration

the sabr parameters are calibrated by fitting the
hagan implied volatility approximation to the market
implied volatility smile.

the calibration is formulated as a nonlinear least squares
problem, where the residuals are the differences between
model and market implied volatilities across strikes.

this file calibrates alpha, rho, and nu while beta is fixed.
beta can be chosen as 0.0, 0.5, or 1.0.
'''

import numpy as np

from src.sabr_iv import sabr_iv


def sabr_sse_alpha_rho_nu(
    alpha,
    rho,
    nu,
    f,
    k_arr,
    t,
    iv_arr,
    beta,
):
    '''
    routine use
        compute sum of squared errors for SABR implied volatility fit

    inputs
        alpha: scalar, SABR volatility level
        rho: scalar, SABR correlation
        nu: scalar, SABR volatility of volatility
        f: scalar, forward price
        k_arr: 1d array (n), strike prices
        t: scalar, time to expiration
        iv_arr: 1d array (n), market implied volatilities
        beta: scalar, fixed SABR beta

    returns
        sse: scalar, sum of squared errors
    '''

    n = len(k_arr)

    sse = 0.0

    if alpha <= 0.0:
        return np.inf

    if rho <= -1.0 or rho >= 1.0:
        return np.inf

    if nu <= 0.0:
        return np.inf

    for i in range(n):

        k_i = k_arr[i]
        iv_i = iv_arr[i]

        model_iv = sabr_iv(
            f,
            k_i,
            t,
            alpha,
            beta,
            rho,
            nu,
        )

        if np.isnan(model_iv):
            return np.inf

        error = model_iv - iv_i

        sse = sse + error*error

    return sse


def sabr_calibr_alpha_rho_nu_grid(
    f,
    k_arr,
    t,
    iv_arr,
    beta,
    alpha_min=0.001,
    alpha_max=10.0,
    n_alpha=20,
    rho_min=-0.99,
    rho_max=0.99,
    n_rho=20,
    nu_min=0.001,
    nu_max=5.0,
    n_nu=20,
):
    '''
    routine use
        calibrate alpha, rho, and nu by grid search

    inputs
        f: scalar, forward price
        k_arr: 1d array (n), strike prices
        t: scalar, time to expiration
        iv_arr: 1d array (n), market implied volatilities
        beta: scalar, fixed SABR beta
        alpha_min: scalar, lower bound for alpha
        alpha_max: scalar, upper bound for alpha
        n_alpha: scalar, number of alpha grid points
        rho_min: scalar, lower bound for rho
        rho_max: scalar, upper bound for rho
        n_rho: scalar, number of rho grid points
        nu_min: scalar, lower bound for nu
        nu_max: scalar, upper bound for nu
        n_nu: scalar, number of nu grid points

    returns
        params: tuple, calibrated parameters (alpha, beta, rho, nu)
        best_sse: scalar, best sum of squared errors
    '''

    alpha_grid = np.linspace(
        alpha_min,
        alpha_max,
        n_alpha,
    )

    rho_grid = np.linspace(
        rho_min,
        rho_max,
        n_rho,
    )

    nu_grid = np.linspace(
        nu_min,
        nu_max,
        n_nu,
    )

    best_alpha = alpha_grid[0]
    best_rho = rho_grid[0]
    best_nu = nu_grid[0]
    best_sse = np.inf

    for i in range(n_alpha):

        alpha_i = alpha_grid[i]

        for j in range(n_rho):

            rho_j = rho_grid[j]

            for l in range(n_nu):

                nu_l = nu_grid[l]

                sse = sabr_sse_alpha_rho_nu(
                    alpha_i,
                    rho_j,
                    nu_l,
                    f,
                    k_arr,
                    t,
                    iv_arr,
                    beta,
                )

                if sse < best_sse:

                    best_sse = sse
                    best_alpha = alpha_i
                    best_rho = rho_j
                    best_nu = nu_l

    params = (
        best_alpha,
        beta,
        best_rho,
        best_nu,
    )

    return params, best_sse


def sabr_calibr_beta_cases(
    f,
    k_arr,
    t,
    iv_arr,
):
    '''
    routine use
        calibrate alpha, rho, and nu for beta equal to 0.0, 0.5, and 1.0

    inputs
        f: scalar, forward price
        k_arr: 1d array (n), strike prices
        t: scalar, time to expiration
        iv_arr: 1d array (n), market implied volatilities

    returns
        results: list, each element is (beta, alpha, rho, nu, sse)
    '''

    beta_arr = np.array(
        [
            0.0,
            0.5,
            1.0,
        ]
    )

    results = []

    for i in range(len(beta_arr)):

        beta_i = beta_arr[i]

        params, sse = sabr_calibr_alpha_rho_nu_grid(
            f,
            k_arr,
            t,
            iv_arr,
            beta_i,
        )

        alpha_i = params[0]
        rho_i = params[2]
        nu_i = params[3]

        result_i = (
            beta_i,
            alpha_i,
            rho_i,
            nu_i,
            sse,
        )

        results.append(result_i)

    return results