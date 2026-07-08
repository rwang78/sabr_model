import os
import pandas as pd

from src.calibr import sabr_calibr_beta_cases


# market data

ticker = "SPY"

expiry = "2026-08-21"

spot = 751.280029296875

t = 0.1232876712328767


# input data

csv_file = (
    "results/tables/"
    "SPY_2026-08-21_computed_iv.csv"
)


def main():
    '''
    routine use
        obtain calibrated SABR parameters using computed Black implied volatility

    inputs
        none

    returns
        none
    '''

    iv_table = pd.read_csv(
        csv_file,
    )

    iv_table = iv_table.dropna(
        subset=[
            "computed_impliedVolatility",
        ]
    )

    k_arr = iv_table["strike"].values

    iv_arr = iv_table["computed_impliedVolatility"].values

    results = sabr_calibr_beta_cases(
        spot,
        k_arr,
        t,
        iv_arr,
    )

    param_rows = []

    for i in range(len(results)):

        beta_i = results[i][0]
        alpha_i = results[i][1]
        rho_i = results[i][2]
        nu_i = results[i][3]
        sse_i = results[i][4]

        param_rows.append(
            {
                "ticker": ticker,
                "expiry": expiry,
                "t": t,
                "spot": spot,
                "beta": beta_i,
                "alpha": alpha_i,
                "rho": rho_i,
                "nu": nu_i,
                "sse": sse_i,
            }
        )

    param_table = pd.DataFrame(
        param_rows,
    )

    output_dir = "results/tables"

    os.makedirs(
        output_dir,
        exist_ok=True,
    )

    output_file = (
        output_dir
        + "/"
        + ticker
        + "_"
        + expiry
        + "_sabr_params_computed_iv.csv"
    )

    param_table.to_csv(
        output_file,
        index=False,
    )

    print(param_table)

    print()
    print("saved to")
    print(output_file)


if __name__ == "__main__":
    main()

'''
  ticker      expiry         t        spot  beta      alpha       rho        nu       sse
0    SPY  2026-08-21  0.123288  751.280029   0.0  10.000000 -0.260526  5.000000  0.840300
1    SPY  2026-08-21  0.123288  751.280029   0.5   3.684842 -0.573158  2.105842  0.008537
2    SPY  2026-08-21  0.123288  751.280029   1.0   6.842421 -0.885789  5.000000  0.362051

saved to
results/tables/SPY_2026-08-21_sabr_params_computed_iv.csv
'''