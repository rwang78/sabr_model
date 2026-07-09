import numpy as np


def black_forward_path_arr(
    f,
    sigma,
    t,
    n_paths,
    n_steps,
    seed=0,
):
    '''
    routine use
        generate Monte Carlo forward price paths under
        Black forward dynamics

    inputs
        f: scalar, initial forward price
        sigma: scalar, Black volatility
        t: scalar, time to expiration
        n_paths: scalar, number of Monte Carlo paths
        n_steps: scalar, number of time steps
        seed: scalar, random seed

    returns
        path_arr: 2d array (n_paths, n_steps + 1), simulated forward price paths
    '''

    rng = np.random.default_rng(
        seed
    )

    dt = t/n_steps

    sqrt_dt = np.sqrt(
        dt
    )

    path_arr = np.zeros(
        (
            n_paths,
            n_steps + 1,
        )
    )

    path_arr[:, 0] = f

    for i in range(n_paths):

        for j in range(n_steps):

            z = rng.normal()

            path_arr[i, j + 1] = (
                path_arr[i, j]
                * np.exp(
                    -0.5*sigma*sigma*dt
                    + sigma*sqrt_dt*z
                )
            )

    return path_arr