import numpy as np

from tests.sabr_inputs import (
    f,
    k,
    t,
    alpha,
    beta,
    rho,
    nu,
    tol,
    n_samples,
    f_arr,
    k_arr,
    t_arr,
    alpha_arr,
    beta_arr,
    rho_arr,
    nu_arr,
)

from src.sabr_iv import (
    sabr_iv,
    sabr_iv_atm,
)

from utils.check_close import check_close


def test_sabr_atm_iv():
    '''
    routine use
        compare general SABR implied volatility with ATM SABR implied volatility

    inputs
        none

    returns
        passed: bool
    '''

    value = sabr_iv(
        f,
        k,
        t,
        alpha,
        beta,
        rho,
        nu,
    )

    target = sabr_iv_atm(
        f,
        t,
        alpha,
        beta,
        rho,
        nu,
    )

    passed = check_close(
        'test SABR ATM implied volatility',
        value,
        target,
        tol,
    )

    return passed


def test_random_sabr_iv_finite():
    '''
    routine use
        test SABR implied volatility is finite on random inputs

    inputs
        none

    returns
        passed: bool
    '''

    passed = True

    for i in range(n_samples):
        sigma_i = sabr_iv(
            f_arr[i],
            k_arr[i],
            t_arr[i],
            alpha_arr[i],
            beta_arr[i],
            rho_arr[i],
            nu_arr[i],
        )

        if np.isnan(sigma_i):
            print('random SABR implied volatility failed')
            print('sample =', i)
            print('sigma =', sigma_i)
            passed = False

        elif sigma_i <= 0.0:
            print('random SABR implied volatility failed')
            print('sample =', i)
            print('sigma =', sigma_i)
            passed = False

    if passed:
        print('random SABR implied volatility passed')
    else:
        print('random SABR implied volatility failed')

    return passed


def main():
    passed = True

    passed = test_sabr_atm_iv() and passed
    passed = test_random_sabr_iv_finite() and passed

    print()

    if passed:
        print('all tests passed')
    else:
        print('some tests failed')


if __name__ == '__main__':
    main()


'''
test SABR ATM implied volatility
value = 0.20179000000000002
target = 0.20179000000000002
error = 0.0
random SABR implied volatility passed

all tests passed
'''