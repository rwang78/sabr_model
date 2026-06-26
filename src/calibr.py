'''
routines for sabr parameter calibration

The sabr parameters are calibrated by fitting the
Hagan implied volatility approximation to the market
implied volatility smile. 

The calibration is formulated
as a nonlinear least squares problem, where the residuals
are the differences between model and market implied
volatilities across strikes.
'''

import numpy as np

from src.model_sabr import sabr_iv




def sabr_calibr(
):
    '''
    calibrate SABR parameters to market implied volatilities

    inputs

    returns
        params: tuple, calibrated parameters
    '''

    pass