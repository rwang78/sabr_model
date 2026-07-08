def filter_option_data(
    option_table,
    spot,
    strike_ratio_low,
    strike_ratio_high,
    min_bid,
    min_ask,
    min_volume,
    min_open_interest,
):
    '''
    routine use
        filter option chain for liquid strikes near the money

    inputs
        option_table: dataframe, option chain
        spot: scalar, current spot price
        strike_ratio_low: scalar, lower strike ratio
        strike_ratio_high: scalar, upper strike ratio
        min_bid: scalar, minimum bid
        min_ask: scalar, minimum ask
        min_volume: scalar, minimum trading volume
        min_open_interest: scalar, minimum open interest

    returns
        filtered_table: dataframe, filtered option chain
    '''

    strike_low = strike_ratio_low*spot

    strike_high = strike_ratio_high*spot

    filtered_table = option_table.copy()

    filtered_table = filtered_table[
        filtered_table["strike"] >= strike_low
    ]

    filtered_table = filtered_table[
        filtered_table["strike"] <= strike_high
    ]

    filtered_table = filtered_table[
        filtered_table["bid"] >= min_bid
    ]

    filtered_table = filtered_table[
        filtered_table["ask"] >= min_ask
    ]

    filtered_table = filtered_table[
        filtered_table["volume"] >= min_volume
    ]

    filtered_table = filtered_table[
        filtered_table["openInterest"] >= min_open_interest
    ]

    filtered_table = filtered_table.copy()

    filtered_table["mid"] = (
        filtered_table["bid"]
        + filtered_table["ask"]
    )/2.0

    return filtered_table