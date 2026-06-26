import numpy as np

from src.model_black import (
    black_call,
    black_put,
    black_call_delta,
    black_put_delta,
#    black_vega,
#    black_volga,
#    black_vanna,
)

from utils.check_close import check_close



f = 100
k = 100
sigma = 0.2
t = 1.0
df = np.exp(-0.05*t)

c0 = 10.450583572185565 # for reference test

tol = 1e-8



def test_black_call(target):
    '''
    compare call price against target value

    inputs
        target: scalar, reference call price

    returns
        bool
    '''

    value = black_call(f, k, sigma, t, df)

    return check_close(
        'test call price',
        value,
        target,
        tol,
    )


def test_put_call_parity():
    '''
    test put call parity under forward measure

    inputs
        none

    returns
        bool
    '''

    call = black_call(f, k, sigma, t, df)
    put = black_put(f, k, sigma, t, df)

    lhs = put
    rhs = call + df*(k - f)

    return check_close(
        'put call parity',
        lhs,
        rhs,
        tol,
    )


def test_delta_parity():
    '''
    test call delta minus put delta under forward measure

    inputs
        none

    returns
        bool
    '''

    call_delta = black_call_delta(f, k, sigma, t, df)
    put_delta = black_put_delta(f, k, sigma, t, df)

    lhs = call_delta - put_delta
    rhs = df

    return check_close(
        'delta parity',
        lhs,
        rhs,
        tol,
    )


if __name__ == '__main__':
    test_black_call(c0)
    test_put_call_parity()
    test_delta_parity()


'''
if
    black_vega,
    black_volga,
    black_vanna,
need to be used, also need to test them 
'''