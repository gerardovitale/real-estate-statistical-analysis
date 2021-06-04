from typing import List, Tuple
import warnings

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats._continuous_distns import _distn_names
from tqdm.notebook import tqdm

from idealista.resources.decorators.timeout_error import timeout


def get_distribution_name_list() -> List[str]:
    return [distribution_name for distribution_name in _distn_names]


def calculate_edf(data: np.ndarray) -> np.ndarray:
    edf = np.arange(1/data.shape[0], 1+1/data.shape[0], 1/data.shape[0])
    return edf


@timeout(30)
def fit_distibution_ks(data: np.ndarray, distribution_name: str) \
    -> Tuple[float, float, Tuple[float]]:
    dist = getattr(stats, distribution_name)
    params = dist.fit(data)
    d_statistic, p_value = stats.kstest(data, distribution_name, args=params)
    return d_statistic, p_value, params


def find_best_fit_based_ks(data: np.ndarray) -> List[List[str]]:
    distribution_list = get_distribution_name_list()
    result = []
    result = {'distribution': None, 'd_statistic': 1, 'p_value': 0, 'params': None}
    for distribution_name in tqdm(distribution_list):
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')
                d_statistic, p_value, params = fit_distibution_ks(data, distribution_name)
                if result['d_statistic'] > d_statistic and result['p_value'] < p_value:
                    result['distribution'] = distribution_name
                    result['d_statistic'] = d_statistic
                    result['p_value'] = p_value
                    result['params'] = params
        except Exception:
            pass
    return result


@timeout(30)
def fit_distibution(dist, data, x, y, max_err=False):
    params = dist.fit(data)
    # Separate parts of parameters
    arg, loc, scale = params[:-2], params[-2], params[-1]
    # Calculate fitted PDF and error with fit in dist
    pdf = dist.pdf(x, loc=loc, scale=scale, *arg)
    sse = np.amax((y - pdf) ** 2) if max_err else np.sum((y - pdf) ** 2)
    return params, pdf, sse
# #calculate absolute difference
# arr_dif_abs = np.abs(cdf - edf)
# #get max different
# dn_ks = max(arr_dif_abs)
# dn_ks


def find_best_distribution(data, ax=None) -> Tuple[str, Tuple[float]]:
    """Model data by finding best fit distribution to data"""
    distribution_list = get_distribution_name_list()
    # Get histogram of original data
    y, x = np.histogram(data, density=True)
    x = (x + np.roll(x, -1))[:-1] / 2.0
    best_distribution = stats.norm
    best_params = (0.0, 1.0)
    best_sse = np.inf
    for distribution_name in tqdm(distribution_list):
        try:
            # Ignore warnings from data that can't be fit
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')
                # print(f"[INFO] evaluating {distribution_name} \
                #     {distribution_list.index(distribution_name)}/{len(distribution_list)}")
                dist = getattr(stats, distribution_name)
                params, pdf, sse = fit_distibution(dist, data, x, y)
                if best_sse > sse and sse > 0:
                    best_distribution = distribution_name
                    best_params = params
                    best_sse = sse
        except Exception:
            pass
    return best_distribution, best_params


def calculate_pdf(distribution_name: str, params: Tuple[float], size=1000) \
    -> Tuple[np.ndarray, np.ndarray]:
    arg, loc, scale = params[:-2], params[-2], params[-1]
    dist = getattr(stats, distribution_name)
    start = dist.ppf(0.01, *arg, loc=loc, scale=scale) \
        if arg else dist.ppf(0.01, loc=loc, scale=scale)
    end = dist.ppf(0.99, *arg, loc=loc, scale=scale) \
        if arg else dist.ppf(0.99, loc=loc, scale=scale)
    x = np.linspace(start, end, size)
    y = dist.pdf(x, loc=loc, scale=scale, *arg)
    return x, y


def calculate_cdf(data: np.ndarray, distribution_name: str, params: Tuple[float]):
    arg, loc, scale = params[:-2], params[-2], params[-1]
    dist = getattr(stats, distribution_name)
    return dist.cdf(data, loc=loc, scale=scale, *arg)
