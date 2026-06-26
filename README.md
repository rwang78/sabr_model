an SABR model validation 

# problem

This project studies option pricing and delta hedging under the SABR stochastic volatility model.

The workflow starts from market option prices, computes the corresponding Black implied volatilities, calibrates the SABR parameters using Hagan's asymptotic volatility formula, and compares the model with a constant volatility Black benchmark.

# structure 

`src/`
    model_black.py      Black pricing formulas and Greeks
    model_imp_vol.py    Black implied volatility routines
    model_sabr.py       Hagan SABR implied volatility and SABR pricing

    data.py             download option chains and build market IV table

    calibr.py            SABR parameter calibration

    comp_pricing.py      pricing comparison
    comp_hedging.py      Monte Carlo hedging comparison

    eval_err.py          pricing and hedging error evaluation

    plot.py              plotting routines

`drivers/`
    run_pricing.py       run monte carlo pricing comparison and save outputs
    run_hedging.py       run monte carlo hedging comparison and save outputs

    run the drivers from the project root for example 
    `python -m drivers.run_pricing`

`tests/`                 test files to validate accuracy of src files 
    test_black.py
    test_imp_vol.py
    test_sabr.py
    test_calibr.py

`utils/`      shared utility functions (rmse, absolution error, etc.)

`results/`
    tables/
    figures/

`sandbox/`    temporary codes 