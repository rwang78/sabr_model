import os

from data.option_download import download_option_chain

ticker = "SPY"

#target_days = 45
# choose the expiration date close to this target 
expiry = "2026-08-21"


def main():
    '''
    routine use
        download an option chain and save it to a csv file

    inputs
        none

    returns
        none
    '''

    spot, _, t, option_table = download_option_chain(
        ticker,
        expiry,
    )

    # t = time to expiration

    print("spot =", spot)
    print("expiry =", expiry)
    print("time =", t)

    print()
    print("columns:")
    print(option_table.columns)

    print()
    print(option_table)

    output_dir = "data"

    os.makedirs(
        output_dir,
        exist_ok=True,
    )

    output_file = (
        f"{output_dir}/"
        f"{ticker}_{expiry}_option_chain.csv"
    )

    option_table.to_csv(
        output_file,
        index=False,
    )

    print()
    print("saved to")
    print(output_file)


if __name__ == "__main__":
    main()


'''
  ticker      expiry         t        spot  beta      alpha       rho   nu       sse
0    SPY  2026-08-21  0.123288  751.280029   0.0  10.000000 -0.900452  0.5  8.220352
1    SPY  2026-08-21  0.123288  751.280029   0.5   5.980302 -0.990000  0.5  0.842422
2    SPY  2026-08-21  0.123288  751.280029   1.0   0.201985 -0.990000  0.5  0.982961

saved to
results/tables/SPY_2026-08-21_sabr_params.csv
(base) wrj@wrj-ThinkPad-E14-Gen-6:~/Dropbox/git_rwang78/sabr_model$ python -m drivers.comp_pricing
     beta  strike  market_mid  market_iv  black_price     sabr_price  black_error  sabr_error
0     0.0   605.0     150.510   0.474859   151.398841   1.462800e+02     0.888841   -4.229971
1     0.5   605.0     150.510   0.474859   151.398841   1.465985e+02     0.888841   -3.911536
2     1.0   605.0     150.510   0.474859   151.398841   1.464150e+02     0.888841   -4.094998
3     0.0   610.0     145.575   0.462713   146.468103   1.412800e+02     0.893103   -4.294971
4     0.5   610.0     145.575   0.462713   146.468103   1.416626e+02     0.893103   -3.912400
..    ...     ...         ...        ...          ...            ...          ...         ...
517   0.5   890.0       0.025   0.167001     0.026903   2.103848e-02     0.001903   -0.003962
518   1.0   890.0       0.025   0.167001     0.026903   1.213568e-02     0.001903   -0.012864
519   0.0   900.0       0.025   0.176766     0.026694  1.649966e-171     0.001694   -0.025000
520   0.5   900.0       0.025   0.176766     0.026694   7.749204e-03     0.001694   -0.017251
521   1.0   900.0       0.025   0.176766     0.026694   4.262986e-03     0.001694   -0.020737

[522 rows x 8 columns]

saved to
results/tables/pricing_table.csv
(base) wrj@wrj-ThinkPad-E14-Gen-6:~/Dropbox/git_rwang78/sabr_model$ python -m data.option_download
(base) wrj@wrj-ThinkPad-E14-Gen-6:~/Dropbox/git_rwang78/sabr_model$ python -m data.run_option_download
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/home/wrj/Dropbox/git_rwang78/sabr_model/data/run_option_download.py", line 66, in <module>
    main()
    ~~~~^^
  File "/home/wrj/Dropbox/git_rwang78/sabr_model/data/run_option_download.py", line 26, in main
    expiry,
    ^^^^^^
UnboundLocalError: cannot access local variable 'expiry' where it is not associated with a value
(base) wrj@wrj-ThinkPad-E14-Gen-6:~/Dropbox/git_rwang78/sabr_model$ python -m data.run_option_download
spot = 748.47998046875
expiry = 2026-08-21
time = 0.12054794520547946

columns:
Index(['contractSymbol', 'lastTradeDate', 'strike', 'lastPrice', 'bid', 'ask',
       'change', 'percentChange', 'volume', 'openInterest',
       'impliedVolatility', 'inTheMoney', 'contractSize', 'currency', 'mid'],
      dtype='object')

         contractSymbol             lastTradeDate  strike  lastPrice  ...  inTheMoney  contractSize  currency      mid
0    SPY260821C00360000 2026-07-06 19:05:52+00:00   360.0     393.71  ...        True       REGULAR       USD  389.400
1    SPY260821C00365000 2026-07-02 14:40:49+00:00   365.0     386.50  ...        True       REGULAR       USD  384.440
2    SPY260821C00370000 2026-04-17 14:32:05+00:00   370.0     343.98  ...        True       REGULAR       USD  370.720
3    SPY260821C00375000 2026-04-07 19:20:29+00:00   375.0     288.49  ...        True       REGULAR       USD  365.400
4    SPY260821C00395000 2026-06-30 16:50:04+00:00   395.0     354.43  ...        True       REGULAR       USD  354.775
..                  ...                       ...     ...        ...  ...         ...           ...       ...      ...
233  SPY260821C00980000 2026-07-02 17:58:09+00:00   980.0       0.01  ...       False       REGULAR       USD    0.005
234  SPY260821C00985000 2026-07-06 13:35:24+00:00   985.0       0.01  ...       False       REGULAR       USD    0.005
235  SPY260821C00990000 2026-06-24 15:04:11+00:00   990.0       0.01  ...       False       REGULAR       USD    0.005
236  SPY260821C00995000 2026-06-26 13:38:17+00:00   995.0       0.01  ...       False       REGULAR       USD    0.005
237  SPY260821C01000000 2026-07-06 13:40:17+00:00  1000.0       0.01  ...       False       REGULAR       USD    0.005

[238 rows x 15 columns]

saved to
data/SPY_2026-08-21_option_chain.csv
'''