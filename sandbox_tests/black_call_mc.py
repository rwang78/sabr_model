import numpy as np

from src.black_call_put_close import black_call

from sandbox_tests.black_call_mc_inputs import load_spy_option_inputs


f, k, sigma, t, df = load_spy_option_inputs()

n_paths = 100
seed = 0


def main():
    '''
    routine use
        test black monte carlo call payouts against black closed form price

    inputs
        none

    returns
        none
    '''

    payout_arr = black_call_payouts(
        f,
        k,
        sigma,
        t,
        df,
        n_paths,
        seed,
    )

    mc_price = np.mean(payout_arr)

    closed_price = black_call(
        f,
        k,
        sigma,
        t,
        df,
    )

    error = abs(mc_price - closed_price)

    print("black call monte carlo test")
    print("f =", f)
    print("k =", k)
    print("sigma =", sigma)
    print("t =", t)
    print("df =", df)
    print("closed price =", closed_price)
    print("mc price =", mc_price)
    print("error =", error)

    if error < 0.50:
        print("pass")
    else:
        print("fail")


if __name__ == "__main__":
    main()