import os

from data.option_download import download_option_chain
from data.option_filter import filter_option_data

ticker = "SPY"

#target_days = 45

expiry = expiry = "2026-08-21"

strike_ratio_low = 0.8

strike_ratio_high = 1.2

min_bid = 0.01

min_ask = 0.01

min_volume = 1

min_open_interest = 1


def main():
    '''
    routine use
        download and filter an option chain, then save the filtered data

    inputs
        none

    returns
        none
    '''

    spot, _, t, option_table = download_option_chain(
        ticker,
        expiry,
    )

    filtered_table = filter_option_data(
        option_table,
        spot,
        strike_ratio_low,
        strike_ratio_high,
        min_bid,
        min_ask,
        min_volume,
        min_open_interest,
    )

    print("spot =", spot)
    print("expiry =", expiry)
    print("time =", t)

    print()
    print("columns:")
    print(filtered_table.columns)

    print()
    print(filtered_table)

    output_dir = "data"

    os.makedirs(
        output_dir,
        exist_ok=True,
    )

    output_file = (
        f"{output_dir}/"
        f"{ticker}_{expiry}_filtered_option_chain.csv"
    )

    filtered_table.to_csv(
        output_file,
        index=False,
    )

    print()
    print("saved to")
    print(output_file)


if __name__ == "__main__":
    main()


'''
spot = 748.719970703125
expiry = 2026-08-21
time = 0.12054794520547946

columns:
Index(['contractSymbol', 'lastTradeDate', 'strike', 'lastPrice', 'bid', 'ask',
       'change', 'percentChange', 'volume', 'openInterest',
       'impliedVolatility', 'inTheMoney', 'contractSize', 'currency', 'mid'],
      dtype='object')

         contractSymbol             lastTradeDate  strike  lastPrice  ...  inTheMoney  contractSize  currency      mid
41   SPY260821C00600000 2026-07-06 14:13:26+00:00   600.0     152.98  ...        True       REGULAR       USD  151.240
42   SPY260821C00605000 2026-07-07 14:30:36+00:00   605.0     145.90  ...        True       REGULAR       USD  146.245
43   SPY260821C00610000 2026-07-01 14:38:05+00:00   610.0     141.04  ...        True       REGULAR       USD  140.995
44   SPY260821C00615000 2026-06-24 15:13:01+00:00   615.0     129.95  ...        True       REGULAR       USD  136.750
45   SPY260821C00620000 2026-06-26 13:57:24+00:00   620.0     117.45  ...        True       REGULAR       USD  131.740
..                  ...                       ...     ...        ...  ...         ...           ...       ...      ...
212  SPY260821C00855000 2026-07-07 14:51:21+00:00   855.0       0.04  ...       False       REGULAR       USD    0.045
213  SPY260821C00860000 2026-07-07 14:25:22+00:00   860.0       0.04  ...       False       REGULAR       USD    0.035
214  SPY260821C00870000 2026-07-06 19:36:47+00:00   870.0       0.04  ...       False       REGULAR       USD    0.035
215  SPY260821C00880000 2026-07-07 15:24:35+00:00   880.0       0.03  ...       False       REGULAR       USD    0.025
216  SPY260821C00890000 2026-07-07 15:13:40+00:00   890.0       0.02  ...       False       REGULAR       USD    0.025

[175 rows x 15 columns]

saved to
results/tables/SPY_2026-08-21_filtered_option_chain.csv
'''