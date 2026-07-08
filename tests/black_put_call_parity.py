import numpy as np

from tests.black_inputs import (
    tol,
    n_samples,
    f_arr,
    k_arr,
    sigma_arr,
    t_arr,
    df_arr,
)

from src.black_call_put_close import (
    black_call,
    black_put,
)


def test_random_put_call_parity():
    '''
    routine use
        test Black put call parity on random inputs

    inputs
        none

    returns
        passed: bool
    '''

    passed = True

    for i in range(n_samples):
        f_i = f_arr[i]
        k_i = k_arr[i]
        sigma_i = sigma_arr[i]
        t_i = t_arr[i]
        df_i = df_arr[i]

        call = black_call(
            f_i,
            k_i,
            sigma_i,
            t_i,
            df_i,
        )

        put = black_put(
            f_i,
            k_i,
            sigma_i,
            t_i,
            df_i,
        )

        lhs = put
        rhs = call + df_i*(k_i - f_i)

        error = abs(lhs - rhs)

        if error > tol:
            print('random put call parity failed')
            print('sample =', i)
            print('f =', f_i)
            print('k =', k_i)
            print('sigma =', sigma_i)
            print('t =', t_i)
            print('df =', df_i)
            print('call =', call)
            print('put =', put)
            print('lhs =', lhs)
            print('rhs =', rhs)
            print('error =', error)
            passed = False

    if passed:
        print('random put call parity passed')
    else:
        print('random put call parity failed')

    return passed


def main():
    passed = True

    passed = test_random_put_call_parity() and passed

    print()

    if passed:
        print('all tests passed')
    else:
        print('some tests failed')


if __name__ == '__main__':
    main()


'''
random put call parity passed

all tests passed
'''