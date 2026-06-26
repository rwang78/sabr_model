# temporary run to look into the data structures
# run with `python -m sandbox.raw_call`

import yfinance as yf

ticker = yf.Ticker('SPY')

expiry = ticker.options[0]

raw_calls = ticker.option_chain(
    expiry,
).calls

print(raw_calls.head(10).to_string(index=False))