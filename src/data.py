import numpy as np
import pandas as pd
import yfinance as yf

from datetime import datetime, timezone

'''
we can look into SPY option chain 

ticker = yf.Ticker('SPY')

expiry = ticker.options[0]

raw_calls = ticker.option_chain(
    expiry,
).calls

print(raw_calls.head(10).to_string(index=False))
'''