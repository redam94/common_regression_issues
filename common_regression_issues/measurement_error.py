"""How to account for the observation process"""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_measurement_error.ipynb.

# %% auto 0
__all__ = ['random_walk_awareness_model', 'survey_obs_model', 'simulate_awareness_survey_data', 'plot_survey_sim_data']

# %% ../nbs/00_measurement_error.ipynb 5
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pymc as pm
from sklearn.metrics import mean_squared_error, r2_score
import statsmodels.api as sm
import xarray as xr
from tueplots import bundles
from tueplots.constants.color import rgb
from .utils.plotting import rgb_to_hex

# %% ../nbs/00_measurement_error.ipynb 9
def random_walk_awareness_model(
  periods: list | pd.DatetimeIndex | np.ndarray, # Time periods to simulate
  ) -> pm.Model: # PyMC model for the random walk awareness model
    coords = {
      'Period': periods,
    }
    with pm.Model(coords = coords) as model:
        #Random walk model
        weekly_variation = pm.HalfNormal('weekly_variation', sigma=.1)
        initial_awareness = pm.Normal('initial_awareness', mu=0, sigma=1)
        logit_awareness = pm.GaussianRandomWalk(
          'logit_awareness', 
          sigma=weekly_variation, 
          init_dist=pm.Normal.dist(mu=initial_awareness, sigma=.01), 
          dims="Period")
        
        weekly_shock = pm.HalfNormal('weekly_shock', sigma=.1)
        _noise = pm.Normal('_noise', mu=0, sigma=1, dims="Period")
        awareness = pm.Deterministic('awareness', pm.math.invlogit(logit_awareness + weekly_shock*_noise), dims="Period")
    return model

# %% ../nbs/00_measurement_error.ipynb 12
def survey_obs_model(
  population_awareness: xr.DataArray | pm.pytensorf.TensorVariable, # Population awareness
  avg_weekly_participants: float = 500.0, # Average number of participants per week
  coords: dict = None, # Coordinates for the PyMC model
  model: pm.Model = None, # PyMC model to add the survey observation model
  ) -> pm.Model:
    if coords is None:
      assert isinstance(population_awareness, xr.DataArray), "If coords is not provided, population_awareness must be an xarray DataArray"
      coords = {
        'Period': population_awareness['Period'].values,
      }
      population_awareness = population_awareness.values
    try:
      model = pm.modelcontext(model)
    except TypeError:
      model = pm.Model(coords=coords)
    with model:
        N_survey_participant = pm.Poisson('n_survey_participants', avg_weekly_participants, dims="Period")
        N_positive = pm.Binomial('n_positive', N_survey_participant, population_awareness, dims="Period")
    return model

# %% ../nbs/00_measurement_error.ipynb 13
def simulate_awareness_survey_data(
  start_date: str = '2020-01-01', # Start date of the survey data
  n_weeks: int = 156, # Number of weeks to simulate
  avg_weekly_participants: float = 500.0, # Average number of participants per week
  weekly_awareness_variation: float = 0.08, # Std. dev. of gaussian inovations for weekly awareness
  starting_population_aware: float = 0.025, # Starting population awareness
  weekly_shock: float = 0.01, # Std. dev. of gaussian noise for weekly deviation from random walk
  random_seed: int = 42, # Random seed for reproducibility
) -> xr.Dataset: # Simulated awareness survey data as an xarray dataset
  dates = pd.date_range(start=start_date, periods=n_weeks, freq='W-MON')
  awareness_model = random_walk_awareness_model(dates)
  gen_model = pm.do(
    awareness_model, 
    {
      'weekly_variation': weekly_awareness_variation, 
      'initial_awareness': np.log(starting_population_aware/(1-starting_population_aware)),
      'weekly_shock': .01
    }
  )
  
  with gen_model:
    survey_obs_model(gen_model['awareness'], avg_weekly_participants=avg_weekly_participants, coords={'Period': dates})
    trace = pm.sample_prior_predictive(1, random_seed=random_seed)
  
  trace = trace.prior.isel(chain=0, draw=0).drop_vars('chain').drop_vars('draw')
  return trace.assign(estimated_awareness = trace['n_positive']/trace['n_survey_participants'])


# %% ../nbs/00_measurement_error.ipynb 14
def plot_survey_sim_data(
  data: xr.Dataset, # Simulated survey data must contain 'awareness' and 'estimated_awareness' variables
) -> None: # Plot of the simulated survey data
    #plt.figure(figsize=(10, 5))
    data.estimated_awareness.plot.scatter(x='Period', color=rgb_to_hex(rgb.tue_gray*256), label='Simulated Survey Data')
    data.awareness.plot(color=rgb_to_hex(rgb.tue_darkgreen*256), ls='--', label="Population Awareness")
    plt.legend()
    plt.title('Simulated Awareness Survey Data');
