"""Random number generation utilities.

Functions:
generate_entropy
reduce_entropy

Classes:
HybridRNG - RNG with both SciPy stats and NumPy random capabilities.
HRNGPackageMethod - For making calls to external libraries in HybridRNG.
HRNGPMRandom - For HybridRNG calls to numpy.random package.
HRNGPMStats - For HybridRNG calls to scipy.stats package.
CauchyPerturber - Forecast error generator based on Cauchy distribution.
"""

import secrets

import numpy as np
from numpy import random
from scipy import stats


# Number of bits used for entropy (NumPy >= 1.18).
# This is limited by what SQLite (v. 3) can handle:
#   https://stackoverflow.com/a/4448400/7232335
#       "Minimum is -(2^63) == -9223372036854775808 and maximum is
#       2^63 - 1 == 9223372036854775807"
#       This is for a signed int, which is what SQLite stores for
#       INTEGER types.
#   https://www.sqlite.org/datatype3.html
#       "INTEGER. The value is a signed integer, stored in 1, 2, 3, 4,
#       6, or 8 bytes depending on the magnitude of the value."
#       8 bytes = 64 bits.  But since one bit must be used for the sign,
#       we are limited to 63-bit entropy values.  Still, 63 bits is
#       plenty.
N_ENTROPY_BITS = 63

# Number of bits SciPy can use.
# SciPy distributions still use NumPy's RandomState object, which is
# limited to a 32-bit entropy representation.
# This comes into play when sampling from PDFs, as SciPy (not NumPy) is
# the package that contains this functionality.
N_SCIPY_BITS = 32

# Functions for entropy generation.

def generate_entropy():
    return secrets.randbits(N_ENTROPY_BITS)

def reduce_entropy(entropy):
    """Maps the given entropy value to a 32-bit value."""
    return entropy % 2**N_SCIPY_BITS

# SUMMARY:
# For NumPy methods such as Generator.choice() and
# Generator.uniform(), a Generator instance, which can be seeded based
# on the larger entropy value, can be used. E.g.:
#
#   entropy = generate_entropy()
#   seed_seq = np.random.SeedSequence(entropy=entropy)
#   rng = np.random.default_rng(seed=seed_seq)
#   sample = rng.uniform()
#
# For SciPy methods such as those having to do with PDFs, a NumPy
# RandomState object must be used, which can only be seeded based on the
# smaller entropy value. E.g.:
#
#   rs = np.random.RandomState(seed=reduce_entropy(entropy))
#   sample = scipy.stats.betaprime.rvs(a=3, b=5, random_state=rs)


class HybridRNG:
    """For generating random numbers for both SciPy probabilities and
    NumPy functionalities. Use the random and stats properties to call
    functions from numpy.random and scipy.stats packages, respectively.
    """

    def __init__(self, entropy=None):
        self.entropy = entropy if entropy is not None else generate_entropy()
        seed_seq = random.SeedSequence(entropy=self.entropy)
        self.rng = random.default_rng(seed=seed_seq)
        # SciPy distributions still use NumPy's RandomState object,
        # which is limited to a 32-bit entropy representation.
        # Using reduce_entropy() maps the 63-bit entropy to a 32-bit
        # entropy. Although the range of possible entropy values is
        # reduced in this way, the results obtained by using the 64-bit
        # RNG and the 32-bit RandomState to pseudo-randomly generate
        # projects are nonetheless deterministic.
        self.rs32 = random.RandomState(seed=reduce_entropy(self.entropy))

    @property
    def random(self):
        return HRNGPMRandom(self.rng)

    @property
    def stats(self):
        return HRNGPMStats(self.rs32)


class HRNGPackageMethod:
    """For assisting HybridRNG property calls by using the RNG that has
    been primed with a certain entropy value.
    """
    def __init__(self, rng):
        self.rng = rng


class HRNGPMRandom(HRNGPackageMethod):
    """Used to call NumPy random package methods using the RNG that has
    been primed with a certain entropy value.
    """
    def __getattr__(self, name):
        return getattr(self.rng, name)


class HRNGPMStats(HRNGPackageMethod):
    """Used to call SciPy stats package methods using the RNG that has
    been primed with a certain entropy value.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._method = None

    def __getattr__(self, name):
        if self._method:
            self._method = getattr(self._method, name)
        else:
            self._method = getattr(stats, name)
        return self

    def __call__(self, *args, **kwargs):
        return self._method(*args, random_state=self.rng, **kwargs)


class CauchyPerturber:
    """Adds random error to forecasts based on a Cauchy distribution."""

    from scipy.stats import cauchy

    def __init__(self, rng, k, ci=0.90, a=-1, max_hzn=24):
        """Positional arguments:
        rng - (HybridRNG) Random number generator.
        k - (float) Log function y-scale parameter.

        Keyword arguments:
        ci - (float) (Default: 0.90) Reference confidence interval. A
            decimal, not a percentage.
        a - (float) (Default: -1) Log function x-shift parameter.
        max_hzn - (int) (Default: 24) Maximum horizon, in number of
            steps, that will need to be perturbed.
        """
        self.rng = rng
        self.max_hzn = max_hzn  # Referenced in sample().
        # Calculate gamma (Cauchy distribution scale parameter) values
        # that result in confidence interval bounds that increase
        # logarithmically as a function of forecast horizon.
        lower_tail_prob = 1 - (1 - ci) / 2
        hzn = np.arange(1, max_hzn + 1)
        # The confidence interval bound is a function y(x) of horizon:
        #   y = k * ln(x - a)
        # The percent point function (ppf) finds the CDF value that
        # corresponds to the given percentage.  This is a way of finding
        # the positive confidence interval bound.
        self.gamma = (
            k * np.log(hzn - a) / self.cauchy.ppf(lower_tail_prob)
        )

    def sample(self, hzn, offset=None, lower_bound=None, upper_bound=None):
        """Return one or more samples from the Cauchy distribution,
        corresponding to the given horizons.

        Positional arguments:
        hzn - (array-like of int) Horizons to sample for. Values are
            number of steps forecasting ahead.

        Keyword arguments:
        offset - (float) (Default: None) Offset for samples.
        lower_bound - (float) (Default: None) Samples below the lower
            bound will be set to the lower bound.
        upper_bound - (float) (Default: None) Samples above the upper
            bound will be set to the upper bound.
        """
        # Input checks.
        min_hzn = min(hzn)
        if min_hzn < 1:
            raise RuntimeError(
                f"Minimum given horizon {min_hzn} crosses allowable limit of 1"
            )
        max_hzn = max(hzn)
        if max_hzn > self.max_hzn:
            raise RuntimeError(
                f"Maximum given horizon {max_hzn} crosses allowable limit of "
                f"{self.max_hzn}"
            )
        # Return value.
        samples = self.rng.stats.cauchy.rvs(scale=self.gamma[hzn - 1])
        if offset is not None:
            samples += offset
        if lower_bound is not None:
            samples = np.maximum(lower_bound, samples)
        if upper_bound is not None:
            samples = np.minimum(upper_bound, samples)
        return samples
