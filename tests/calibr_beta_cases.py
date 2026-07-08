from tests.calibr_inputs import (
    f,
    t,
    nu,
    k_arr,
    iv_arr,
)

from src.calibr import sabr_calibr_beta_cases


def test_sabr_calibr_beta_cases():
    '''
    routine use
        test SABR calibration runs for beta equal to 0.0, 0.5, and 1.0

    inputs
        none

    returns
        passed: bool
    '''

    results = sabr_calibr_beta_cases(
        f,
        k_arr,
        t,
        iv_arr,
        nu,
    )

    passed = True

    if len(results) != 3:
        print('SABR beta cases failed')
        print('number of results =', len(results))
        passed = False

    beta_target_arr = [
        0.0,
        0.5,
        1.0,
    ]

    for i in range(len(results)):
        result_i = results[i]

        beta_i = result_i[0]
        alpha_i = result_i[1]
        rho_i = result_i[2]
        nu_i = result_i[3]
        sse_i = result_i[4]

        if beta_i != beta_target_arr[i]:
            print('SABR beta case failed')
            print('sample =', i)
            print('beta value =', beta_i)
            print('beta target =', beta_target_arr[i])
            passed = False

        if alpha_i <= 0.0:
            print('SABR beta case failed')
            print('sample =', i)
            print('alpha =', alpha_i)
            passed = False

        if rho_i <= -1.0 or rho_i >= 1.0:
            print('SABR beta case failed')
            print('sample =', i)
            print('rho =', rho_i)
            passed = False

        if nu_i != nu:
            print('SABR beta case failed')
            print('sample =', i)
            print('nu value =', nu_i)
            print('nu target =', nu)
            passed = False

        if sse_i < 0.0:
            print('SABR beta case failed')
            print('sample =', i)
            print('sse =', sse_i)
            passed = False

    if passed:
        print('SABR beta cases passed')
    else:
        print('SABR beta cases failed')

    return passed


def main():
    passed = True

    passed = test_sabr_calibr_beta_cases() and passed

    print()

    if passed:
        print('all tests passed')
    else:
        print('some tests failed')


if __name__ == '__main__':
    main()


'''
SABR beta cases passed
'''