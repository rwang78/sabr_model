# An SABR Model Validation

## problem

This project studies option pricing and delta hedging under the SABR stochastic volatility model.

The workflow starts from market option prices, computes the corresponding Black implied volatilities, calibrates the SABR parameters using Hagan's asymptotic volatility formula, and compares the model with a constant volatility Black benchmark.

## Repository Structure

`src/`

All numerical routines.

`drivers/`

Driver scripts used to reproduce all tables and figures.

`tests/`

Tests for the routines in `src/`.

`utils/`

Shared utility functions, such as RMSE and absolute error.

`results/`

Output tables and figures.

`sandbox/`

Temporary development code.

## Running

Run each driver as

```bash
python -m drivers.<driver_name>
```

Recommended execution order

`data_hedge_input`

Copy the required columns from the downloaded market option data.

`data_black_vol_constant`

Compute the constant volatility used by the Black model.

`black_call`

Compute Black call prices.

`black_imp_vol`

Compute Black implied volatilities.

`calibr`

Calibrate the SABR parameters.

`calibr_add_output`

Append the calibrated parameters to the output table.

`sabr_iv`

Compute Hagan implied volatilities.

`sabr_call`

Compute SABR call prices.

`mc_forward`

Generate forward price paths under the Black and SABR models.

`hedge`

Perform Monte Carlo pricing and dynamic delta hedging.

The plotting drivers can then be executed to reproduce all figures.

## Output

The main output table is

`results/tables/SPY_2026-08-21_hedge_output.csv`

All figures are saved under

`results/figures/`

## Data

The current implementation uses

* Underlying: `SPY`
* Expiration: `2026-08-21`

The workflow can be applied to other option chains by changing the input data.
```