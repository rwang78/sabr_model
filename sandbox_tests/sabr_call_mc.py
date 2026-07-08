import numpy as np

from sabr_mc_call import sabr_call_payouts
from src.sabr_iv import sabr_iv
from src.black_call_put_close import black_call

from sandbox_tests.black_call_mc_inputs import load_spy_option_inputs


f, k, market_sigma, t, df = load_spy_option_inputs()

alpha = 5.980302
beta = 0.5
rho = -0.99
nu = 0.5

n_paths = 100
n_steps = 20
seed = 0


def main():
    '''
    routine use
        test sabr monte carlo call payouts against hagan implied volatility price

    inputs
        none

    returns
        none
    '''

    sabr_sigma = sabr_iv(
        f,
        k,
        t,
        alpha,
        beta,
        rho,
        nu,
    )

    hagan_price = black_call(
        f,
        k,
        sabr_sigma,
        t,
        df,
    )

    payout_arr = sabr_call_payouts(
        f,
        k,
        t,
        df,
        alpha,
        beta,
        rho,
        nu,
        n_paths,
        n_steps,
        seed,
    )

    mc_price = np.mean(payout_arr)

    error = abs(mc_price - hagan_price)

    print("sabr call monte carlo test")
    print("f =", f)
    print("k =", k)
    print("market sigma =", market_sigma)
    print("sabr sigma =", sabr_sigma)
    print("t =", t)
    print("df =", df)
    print("hagan price =", hagan_price)
    print("mc price =", mc_price)
    print("error =", error)

    if error < 2.00:
        print("pass")
    else:
        print("fail")


if __name__ == "__main__":
    main()

'''
sabr call monte carlo test
f = 751.280029296875
k = 728.0
market sigma = 0.1940083041381836
sabr sigma = 0.22696769454158267
t = 0.1232876712328767
df = 1.0
hagan price = 36.95851327263313
mc price = 36.01693981693601
error = 0.9415734556971174
pass
'''