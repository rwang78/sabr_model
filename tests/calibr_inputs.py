import numpy as np

from src.sabr_iv import sabr_iv


f = 100.0
t = 1.0

alpha = 2.0
beta = 0.5
rho = -0.3
nu = 0.4

tol = 1e-8
tol_calibr = 1e-2

k_arr = np.array(
    [
        70.0,
        80.0,
        90.0,
        100.0,
        110.0,
        120.0,
        130.0,
    ]
)

n = len(k_arr)

iv_arr = np.zeros(n)

for i in range(n):
    iv_arr[i] = sabr_iv(
        f,
        k_arr[i],
        t,
        alpha,
        beta,
        rho,
        nu,
    )

