"""Logic for creating forecasts based on applying some forecast error as
sampled from a probability distribution.

Functions:
apply_forecast_error
"""

import re

import numpy as np


def apply_forecast_error(forecast, perturber):
    """Apply forecast error to the given forecast, using the given
    random number generator.

    Positional arguments:
    forecast - (dict) Forecast information with the same structure as
        returned by get_data().
    perturber - (Perturber) Perturber object instance that can produce
        samples from a statistical distribution to be used as the
        applied error.
    """
    # Horizon: Number of steps forecasting ahead.
    horizon = np.arange(1, len(forecast["timestamp"]) + 1)
    # For both demand and weather, limit the sampled multiplier to the
    # range [0.5, 1.5].
    # Define error application function.
    def apply_error(signal, horizon):
        # Divide by 100 to use samples as percents.
        return (
            signal * perturber.sample(
                horizon[:len(signal)],
                offset=1,
                lower_bound=0.5,
                upper_bound=1.5,
            )
        ).tolist()
    # Demand.
    rexp = re.compile("Node[0-9]+")
    node_names = [k for k in forecast if rexp.fullmatch(k)]
    for node in node_names:
        forecast[node]["demand"] = apply_error(
            forecast[node]["demand"], horizon
        )
    # Weather.
    for k in forecast["weather"]:
        # Limit perturbed weather fields since some fields are linked,
        # e.g. t_dryb and t_dewp.  Also, some fields vary on a cyclical
        # scale, e.g. wdir, which is measured in degrees between 0 and
        # 360.
        if k in (
            "glo_horz_irr", "dir_norm_irr", "dif_horz_irr", "t_dryb", "wspd"
        ):
            forecast["weather"][k] = apply_error(
                forecast["weather"][k], horizon
            )
    return forecast
