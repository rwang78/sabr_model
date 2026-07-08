import numpy as np

f = 100.0
k = 100.0
t = 1.0
r = 0.05
df = np.exp(-r*t)

alpha = 2.0
beta = 0.5
rho = -0.3
nu = 0.4

tol = 1e-8
tol_fd = 1e-5

n_samples = 100

rng = np.random.default_rng(0)

f_arr = rng.uniform(
    50.0,
    200.0,
    n_samples,
)

k_arr = rng.uniform(
    50.0,
    200.0,
    n_samples,
)

t_arr = rng.uniform(
    0.05,
    3.0,
    n_samples,
)

r_arr = rng.uniform(
    0.0,
    0.08,
    n_samples,
)

df_arr = np.exp(-r_arr*t_arr)

alpha_arr = rng.uniform(
    0.5,
    5.0,
    n_samples,
)

beta_arr = rng.uniform(
    0.2,
    1.0,
    n_samples,
)

rho_arr = rng.uniform(
    -0.8,
    0.8,
    n_samples,
)

nu_arr = rng.uniform(
    0.05,
    2.0,
    n_samples,
)