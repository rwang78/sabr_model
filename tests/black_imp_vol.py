import numpy as np

from src.black_call_put_close import black_call

from src.black_imp_vol import (
    call_price_error,
    black_call_iv,
    brent_solver,
)

from utils.check_close import check_close


f = 100.0
k = 100.0
sigma = 0.2
t = 1.0
df = np.exp(-0.05 * t)

tol = 1e-8


price = black_call(
    f,
    k,
    sigma,
    t,
    df,
)


def test_call_price_error():
    '''
    test pricing error at the true volatility

    returns
        bool
    '''

    error = call_price_error(
        sigma,
        price,
        f,
        k,
        t,
        df,
    )

    return check_close(
        'call price error',
        error,
        0.0,
        tol,
    )


def test_black_call_iv():
    '''
    test implied volatility recovery

    returns
        bool
    '''

    iv = black_call_iv(
        price,
        f,
        k,
        t,
        df,
        brent_solver,
    )

    return check_close(
        'implied volatility',
        iv,
        sigma,
        tol,
    )


def run_all_tests():
    '''
    run all tests

    returns
        bool
    '''

    results = []

    results.append(test_call_price_error())
    results.append(test_black_call_iv())

    return all(results)


if __name__ == '__main__':
    run_all_tests()


'''one of the outputs: 

call price error
value = 0.0
target = 0.0
error = 0.0
implied volatility
value = 0.20000000000000018
target = 0.2
error = 1.6653345369377348e-16

given the small error the test passes for this case 
'''