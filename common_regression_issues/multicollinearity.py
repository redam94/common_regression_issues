"""A causal example"""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_multicollinearity.ipynb.

# %% auto 0
__all__ = ['sample_random_data']

# %% ../nbs/01_multicollinearity.ipynb 3
import xarray as xr
import pandas as pd
import numpy as np

# %% ../nbs/01_multicollinearity.ipynb 10
def sample_random_data(
    N_weeks: int, # Number of weeks to generate
    include_hidden_confounds:bool=False, # Should hidden confounds be included in the dataset
    random_seed: int|None = None, # Random Seed
) -> xr.Dataset: # Dataset containing the variables described by the above causal model
    t = np.linspace(0, (N_weeks-1)/52., N_weeks)
    dates = pd.date_range("2021-01-01", periods=N_weeks, freq="W-MON")
    rng = np.random.default_rng(random_seed)

    ## Define Seasonal component
    seasonal_coeffs_sin = rng.normal(0, 2, 3)/np.arange(1, 4)**2
    seasonal_coeffs_cos = rng.normal(0, 2, 3)/np.arange(1, 4)**2
    season = (
        np.stack([np.sin(i*2*np.pi*t) for i in range(1, 4)]).T @ seasonal_coeffs_sin
        + np.stack([np.cos(i*2*np.pi*t) for i in range(1, 4)]).T @ seasonal_coeffs_cos
    )
    season = xr.DataArray(season, coords={"Period": dates}, dims="Period")

    ## Define Price Movements
    return season
