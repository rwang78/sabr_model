from tests.black_inputs import (
    n_samples,
    s_arr,
    k_arr,
    sigma_arr,
    t_arr,
    r_arr,
    df_arr,
    tol_fd,
)

from src.black_call_put_close import black_call
from src.black_greeks import black_call_delta


def test_random_call_delta_fd():
    '''
    routine use
        test black call delta against finite difference
        of black call price

    inputs
        none

    returns
        passed: bool
    '''

    passed = True

    for i in range(n_samples):

        s_i = s_arr[i]
        k_i = k_arr[i]
        sigma_i = sigma_arr[i]
        t_i = t_arr[i]
        r_i = r_arr[i]
        df_i = df_arr[i]

        bump = 1e-4*s_i

        price_up = black_call(
            s_i + bump,
            k_i,
            sigma_i,
            t_i,
            df_i,
        )

        price_down = black_call(
            s_i - bump,
            k_i,
            sigma_i,
            t_i,
            df_i,
        )

        delta_fd = (
            price_up
            - price_down
        )/(2.0*bump)

        delta = black_call_delta(
            s_i,
            k_i,
            sigma_i,
            t_i,
            df_i,
        )

        error = abs(
            delta
            - delta_fd
        )

        if error > tol_fd:

            print('random call delta finite difference failed')
            print('sample =', i)
            print('s =', s_i)
            print('k =', k_i)
            print('sigma =', sigma_i)
            print('t =', t_i)
            print('r =', r_i)
            print('df =', df_i)
            print('delta =', delta)
            print('delta_fd =', delta_fd)
            print('error =', error)

            passed = False

    if passed:

        print('random call delta finite difference passed')

    return passed


def main():
    '''
    routine use
        run random finite difference test for Black call delta

    inputs
        none

    returns
        none
    '''

    passed = test_random_call_delta_fd()

    print(
        'test_random_call_delta_fd =',
        passed,
    )


if __name__ == '__main__':

    main()