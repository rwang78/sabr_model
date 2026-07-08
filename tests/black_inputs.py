import numpy as np

# common inputs

f = 100.0
k = 100.0
sigma = 0.2
t = 1.0
r = 0.05
df = np.exp(-r*t)

tol = 1e-8
tol_fd = 1e-6


# for random tests

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

sigma_arr = rng.uniform(
    0.05,
    1.0,
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