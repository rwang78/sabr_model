import numpy as np

from tests.black_inputs import (
    f,
    k,
    sigma,
    t,
    df,
    tol,
    f_arr,
    k_arr,
    sigma_arr,
    t_arr,
    r_arr,
    df_arr,
)

from src.black_call_put_close import (
    black_call,
    black_put,
    black_call_delta,
    black_put_delta,
#    black_vega,
#    black_volga,
#    black_vanna,
)

from utils.check_close import check_close


c0_black = 7.57708214642728


def test_black_call(target):
    '''
    routine use
        compare Black call price against target value

    inputs
        target: scalar, reference call price

    returns
        passed: bool
    '''

    value = black_call(
        f,
        k,
        sigma,
        t,
        df,
    )

    passed = check_close(
        'test call price',
        value,
        target,
        tol,
    )

    return passed


def main():
    passed = True

    passed = test_black_call(c0_black) and passed

    print()

    if passed:
        print('all tests passed')
    else:
        print('some tests failed')


if __name__ == '__main__':
    main()


'''
test call price
value = 7.57708214642728
target = 7.57708214642728
error = 0.0

all tests passed
'''