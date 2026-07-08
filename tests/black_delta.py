from tests.black_inputs import (
    tol,
    n_samples,
    f_arr,
    k_arr,
    sigma_arr,
    t_arr,
    df_arr,
)

from src.black_greeks import (
    black_call_delta,
    black_put_delta,
)


def test_random_delta():
    '''
    routine use
        test Black delta put call parity on random inputs

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

        call_delta = black_call_delta(
            f_i,
            k_i,
            sigma_i,
            t_i,
            df_i,
        )

        put_delta = black_put_delta(
            f_i,
            k_i,
            sigma_i,
            t_i,
            df_i,
        )

        lhs = call_delta - put_delta
        rhs = df_i

        error = abs(lhs - rhs)

        if error > tol:
            print('random delta failed')
            print('sample =', i)
            print('f =', f_i)
            print('k =', k_i)
            print('sigma =', sigma_i)
            print('t =', t_i)
            print('df =', df_i)
            print('call delta =', call_delta)
            print('put delta =', put_delta)
            print('lhs =', lhs)
            print('rhs =', rhs)
            print('error =', error)
            passed = False

    if passed:
        print('random delta passed')
    else:
        print('random delta failed')

    return passed


def main():
    passed = True

    passed = test_random_delta() and passed

    print()

    if passed:
        print('all tests passed')
    else:
        print('some tests failed')


if __name__ == '__main__':
    main()