"""Spline models and samples"""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/model_helpers/01_spline_models.ipynb.

# %% auto 0
__all__ = ['spline_component']

# %% ../../nbs/model_helpers/01_spline_models.ipynb 4
import numpy as np
import pymc as pm
from patsy import dmatrix
import xarray as xr
from typing import TypeVar, List, Iterable

# %% ../../nbs/model_helpers/01_spline_models.ipynb 6
_T = TypeVar("T")

# %% ../../nbs/model_helpers/01_spline_models.ipynb 7
def spline_component(
    knots: int | List[_T], # Number of knots or interior knots to use
    index: Iterable[_T], # index
    degree: int = 3, # Knot degree defaults to cubic splines
):
    if isinstance(knots, int):
        steps = len(index)/(knots)
        knots_ = [index[int(i*steps)] for i in range(knots)]
        knots = knots_[1:-1]
    
    
    splines = dmatrix(
        "bs(x, knots=knots, degree=degree, include_intercept=False)-1", 
        {
            'x': index,
            'knots': knots,
            'degree': degree
        }
    )
    return np.asarray(splines)
    
