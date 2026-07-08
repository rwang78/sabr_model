from tests.calibr_inputs import (
    f,
    t,
    alpha,
    beta,
    rho,
    nu,
    tol,
    k_arr,
    iv_arr,
)

from src.calibr import sabr_sse_alpha_rho


def test_sabr_sse_alpha_rho_true_params():
    '''
    routine use
        test SABR sum of squared errors is zero at true parameters

    inputs
        none

    returns
        passed: bool
    '''

    value = sabr_sse_alpha_rho(
        alpha,
        rho,
        f,
        k_arr,
        t,
        iv_arr,
        beta,
        nu,
    )

    passed = True

    if value > tol:
        print('SABR SSE true parameters failed')
        print('value =', value)
        print('target =', 0.0)
        print('error =', value)
        passed = False

    if passed:
        print('SABR SSE true parameters passed')
    else:
        print('SABR SSE true parameters failed')

    return passed


def test_sabr_sse_alpha_rho_wrong_params():
    '''
    routine use
        test SABR sum of squared errors is positive at wrong parameters

    inputs
        none

    returns
        passed: bool
    '''

    value = sabr_sse_alpha_rho(
        1.5*alpha,
        0.5*rho,
        f,
        k_arr,
        t,
        iv_arr,
        beta,
        nu,
    )

    passed = True

    if value <= tol:
        print('SABR SSE wrong parameters failed')
        print('value =', value)
        passed = False

    if passed:
        print('SABR SSE wrong parameters passed')
    else:
        print('SABR SSE wrong parameters failed')

    return passed


def main():
    passed = True

    passed = test_sabr_sse_alpha_rho_true_params() and passed
    passed = test_sabr_sse_alpha_rho_wrong_params() and passed

    print()

    if passed:
        print('all tests passed')
    else:
        print('some tests failed')


if __name__ == '__main__':
    main()

'''
SABR SSE true parameters passed
SABR SSE wrong parameters passed

all tests passed
'''