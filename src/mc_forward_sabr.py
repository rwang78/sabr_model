import numpy as np


def simulate_sabr_euler_maruyama(
    F0,
    alpha0,
    beta,
    rho,
    nu,
    T,
    N_steps,
    M_paths,
    seed=0,
):
    """
    Simulates the SABR model using the Euler-Maruyama method.

    returns:
        F: 1d array, forward prices 
        alpha: 1d array, parameter for volatility 
    """

    rng = np.random.default_rng(seed)

    dt = T/N_steps
    sqrt_dt = np.sqrt(dt)

    F = np.zeros(
        (
            N_steps + 1,
            M_paths,
        )
    )

    alpha = np.zeros(
        (
            N_steps + 1,
            M_paths,
        )
    )

    # Set initial conditions.

    F[0] = F0
    alpha[0] = alpha0

    for i in range(N_steps):

        # Generate independent standard normal shocks.

        Z1 = rng.standard_normal(M_paths)
        Z3 = rng.standard_normal(M_paths)

        # Construct the correlated shock for volatility.

        Z2 = (
            rho*Z1
            + np.sqrt(1.0 - rho**2)*Z3
        )

        # Euler Maruyama step for volatility.

        alpha_safe = np.maximum(
            alpha[i],
            0.0,
        )

        alpha[i + 1] = np.maximum(
            alpha_safe
            + nu*alpha_safe*sqrt_dt*Z2,
            0.0,
        )

        # Euler Maruyama step for the forward rate.

        F_safe = np.maximum(
            F[i],
            0.0,
        )

        F[i + 1] = np.maximum(
            F_safe
            + alpha_safe*(F_safe**beta)*sqrt_dt*Z1,
            0.0,
        )

    return F, alpha