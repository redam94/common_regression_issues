"""Some common utility functions"""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/utils/00_plotting.ipynb.

# %% auto 0
__all__ = ['rgb_to_hex']

# %% ../../nbs/utils/00_plotting.ipynb 3
import numpy as np

# %% ../../nbs/utils/00_plotting.ipynb 4
def rgb_to_hex(
    color: np.ndarray # Nd array of color values
    ) -> str: # hex string of color data
    """Converts an RGB color array to a hex color string."""
    return "#{:02X}{:02X}{:02X}".format(*color.astype(int))