import numpy as np

from tests.sabr_inputs import (
    tol_fd,
    n_samples,
    f_arr,
    k_arr,
    t_arr,
    df_arr,
    alpha_arr,
    beta_arr,
    rho_arr,
    nu_arr,
)

from src.sabr_iv import (
    sabr_call_price,
    sabr_delta_fd,
)


def test_random_sabr_delta_fd():
    '''
    routine use
        compare SABR delta with finite difference of SABR call price

    inputs
        none

    returns
        passed: bool
    '''

    passed = True

    for i in range(n_samples):
        f_i = f_arr[i]
        k_i = k_arr[i]
        t_i = t_arr[i]
        df_i = df_arr[i]
        alpha_i = alpha_arr[i]
        beta_i = beta_arr[i]
        rho_i = rho_arr[i]
        nu_i = nu_arr[i]

        bump = 1e-4*f_i

        price_up = sabr_call_price(
            f_i + bump,
            k_i,
            t_i,
            alpha_i,
            beta_i,
            rho_i,
            nu_i,
            df_i,
        )

        price_down = sabr_call_price(
            f_i - bump,
            k_i,
            t_i,
            alpha_i,
            beta_i,
            rho_i,
            nu_i,
            df_i,
        )

        delta_fd = (price_up - price_down)/(2.0*bump)

        delta = sabr_delta_fd(
            f_i,
            k_i,
            t_i,
            df_i,
            alpha_i,
            beta_i,
            rho_i,
            nu_i,
            bump,
        )

        error = abs(delta - delta_fd)

        if np.isnan(delta):
            print('random SABR delta failed')
            print('sample =', i)
            print('delta =', delta)
            passed = False

        elif error > tol_fd:
            print('random SABR delta failed')
            print('sample =', i)
            print('f =', f_i)
            print('k =', k_i)
            print('t =', t_i)
            print('df =', df_i)
            print('alpha =', alpha_i)
            print('beta =', beta_i)
            print('rho =', rho_i)
            print('nu =', nu_i)
            print('delta =', delta)
            print('delta_fd =', delta_fd)
            print('error =', error)
            passed = False

    if passed:
        print('random SABR delta passed')
    else:
        print('random SABR delta failed')

    return passed


def main():
    passed = True

    passed = test_random_sabr_delta_fd() and passed

    print()

    if passed:
        print('all tests passed')
    else:
        print('some tests failed')


if __name__ == '__main__':
    main()

'''
random SABR delta passed
'''