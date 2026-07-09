import os
import yfinance as yf


ticker = "SPY"

start_date = "2025-07-01"

end_date = "2026-07-08"

output_file = (
    "data/"
    "SPY_history.csv"
)


def main():
    '''
    routine use
        download historical SPY prices and save them to csv

    inputs
        none

    returns
        none
    '''

    history_table = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False,
    )

    output_dir = os.path.dirname(
        output_file,
    )

    if output_dir != "":
        os.makedirs(
            output_dir,
            exist_ok=True,
        )

    history_table.to_csv(
        output_file,
    )

    print(
        history_table.head()
    )

    print(
        "saved to",
        output_file,
    )


if __name__ == "__main__":

    main()

'''
Ticker             SPY         SPY         SPY         SPY       SPY
Date                                                                
2025-07-01  610.881287  612.048348  608.774624  609.605385  70030100
2025-07-02  613.650635  613.690175  609.852690  610.475791  66510400
2025-07-03  618.487000  619.416701  615.608856  615.628656  51065800
2025-07-07  613.877991  617.191314  611.098788  616.528613  74814500
2025-07-08  613.541809  615.292371  612.730788  614.540690  59024600
saved to data/SPY_history.csv
'''