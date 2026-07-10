# An SABR model validation

## Problem

This project studies option pricing and delta hedging under the SABR stochastic volatility model.

The workflow starts from market option prices, computes the corresponding Black implied volatilities, calibrates the SABR parameters using Hagan's asymptotic volatility formula, and compares the model with a constant volatility Black benchmark

## Structure

`src/`                 all numerical routines

`drivers/`          driver scripts used to reproduce all tables and figures

`tests/`             tests for the routines in `src/`

`utils/`             shared utility functions, such as rmse and absolute error

`results/`          output tables and figures

`sandbox/`       temporary development code

## Running

Run each driver as

```bash
python -m drivers.<driver_name>
```

Recommended execution order

`data_hedge_input`                copy the required columns from the downloaded market option data

`data_black_vol_constant`    compute the constant volatility used by the Black model

`black_call`                            compute Black call prices

`black_imp_vol`                   compute Black implied volatilities

`calibr`                                  calibrate the SABR parameters

`calibr_add_output`         append the calibrated parameters to the output table

`sabr_iv`                             compute Hagan implied volatilities

`sabr_call`                         compute SABR call prices

`mc_forward`                    generate forward price paths under the Black and SABR models

`hedge`                               perform Monte Carlo pricing and dynamic delta hedging

The plotting drivers can then be executed to reproduce all figures

## Output

Main output table

`results/tables/SPY_2026-08-21_hedge_output.csv`

Figures

`results/figures/`

## Data

Current implementation

* underlying: `SPY`
* expiration: `2026-08-21`

The workflow can be applied to other option chains by changing the input data