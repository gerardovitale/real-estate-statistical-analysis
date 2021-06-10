from typing import List, Tuple
import warnings

import numpy as np
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
    result = {'distribution': None, 'd_statistic': 1, 'p_value': 0, 'params': None}
    for distribution_name in tqdm(distribution_list):
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')
                d_statistic, p_value, params = fit_distibution_ks(data, distribution_name)
                if result['p_value'] < p_value:
                    result['distribution'] = distribution_name
                    result['d_statistic'] = d_statistic
                    result['p_value'] = p_value
                    result['params'] = params
        except Exception:
            pass
    return result


@timeout(30)
def fit_distibution(dist, data, x, y, err_type='sse'):
    params = dist.fit(data)
    # Separate parts of parameters
    arg, loc, scale = params[:-2], params[-2], params[-1]
    # Calculate fitted PDF and error with fit in dist
    pdf = dist.pdf(x, loc=loc, scale=scale, *arg)
    if err_type == 'sse':
        err = np.sum((y - pdf) ** 2) 
    elif err_type == 'max_sq_err':
        err = np.amax((y - pdf) ** 2)
    elif err_type == 'max_err':
        err = np.amax(np.abs(y - pdf))
    return pdf, params, err


def find_best_dist(data, err_type='sse') -> Tuple[str, Tuple[float]]:
    """
    Model data by finding best fit distribution to data.
    Where err_type stands for the method used to calculate the difference 
    between the distribution studied
    """
    distribution_list = get_distribution_name_list()
    y, x = np.histogram(data, density=True)
    x = (x + np.roll(x, -1))[:-1] / 2.0
    result = {'distribution': None, 'error': np.inf, 'params': None}
    for distribution_name in tqdm(distribution_list):
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')
                # print(f"[INFO] evaluating {distribution_name} \
                #     {distribution_list.index(distribution_name)}/{len(distribution_list)}")
                dist = getattr(stats, distribution_name)
                pdf, params, err = fit_distibution(dist, data, x, y, err_type=err_type)
                if result['error'] > err and err > 0:
                    result['distribution'] = distribution_name
                    result['params'] = params
                    result['error'] = err
        except Exception:
            pass
    return result


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
