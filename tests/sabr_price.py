from tests.sabr_inputs import (
    f,
    k,
    t,
    df,
    alpha,
    beta,
    rho,
    nu,
    tol,
)

from black_call_put_close import black_call

from src.sabr_iv import (
    sabr_iv
)

from src.sabr_call_close import(
    sabr_call_price
)

from utils.check_close import check_close


def test_sabr_call_price():
    '''
    routine use
        compare SABR call price with Black call price using SABR implied volatility

    inputs
        none

    returns
        passed: bool
    '''

    sigma = sabr_iv(
        f,
        k,
        t,
        alpha,
        beta,
        rho,
        nu,
    )

    value = sabr_call_price(
        f,
        k,
        t,
        alpha,
        beta,
        rho,
        nu,
        df,
    )

    target = black_call(
        f,
        k,
        sigma,
        t,
        df,
    )

    passed = check_close(
        'test SABR call price',
        value,
        target,
        tol,
    )

    return passed


def main():
    passed = True

    passed = test_sabr_call_price() and passed

    print()

    if passed:
        print('all tests passed')
    else:
        print('some tests failed')


if __name__ == '__main__':
    main()

'''
test SABR call price
value = 7.64466824972983
target = 7.64466824972983
error = 0.0

all tests passed
'''