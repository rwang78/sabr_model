from tests.calibr_inputs import (
    f,
    t,
    alpha,
    beta,
    rho,
    nu,
    tol_calibr,
    k_arr,
    iv_arr,
)

from src.calibr import sabr_calibr_alpha_rho_grid


def test_sabr_calibr_alpha_rho_grid():
    '''
    routine use
        test SABR grid calibration recovers alpha and rho approximately

    inputs
        none

    returns
        passed: bool
    '''

    params, sse = sabr_calibr_alpha_rho_grid(
        f,
        k_arr,
        t,
        iv_arr,
        beta,
        nu,
        alpha_min=1.0,
        alpha_max=3.0,
        n_alpha=201,
        rho_min=-0.8,
        rho_max=0.2,
        n_rho=201,
    )

    alpha_value = params[0]
    beta_value = params[1]
    rho_value = params[2]
    nu_value = params[3]

    alpha_error = abs(alpha_value - alpha)
    rho_error = abs(rho_value - rho)

    passed = True

    if alpha_error > tol_calibr:
        print('SABR alpha grid calibration failed')
        print('alpha value =', alpha_value)
        print('alpha target =', alpha)
        print('alpha error =', alpha_error)
        passed = False

    if rho_error > tol_calibr:
        print('SABR rho grid calibration failed')
        print('rho value =', rho_value)
        print('rho target =', rho)
        print('rho error =', rho_error)
        passed = False

    if beta_value != beta:
        print('SABR beta grid calibration failed')
        print('beta value =', beta_value)
        print('beta target =', beta)
        passed = False

    if nu_value != nu:
        print('SABR nu grid calibration failed')
        print('nu value =', nu_value)
        print('nu target =', nu)
        passed = False

    if passed:
        print('SABR alpha rho grid calibration passed')
    else:
        print('SABR alpha rho grid calibration failed')

    return passed


def main():
    passed = True

    passed = test_sabr_calibr_alpha_rho_grid() and passed

    print()

    if passed:
        print('all tests passed')
    else:
        print('some tests failed')


if __name__ == '__main__':
    main()

'''
SABR alpha rho grid calibration passed
'''