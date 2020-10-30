import pytest
import numpy as np
import math


def test_gamma_distribution_produces_expected_mean_and_cv():
    """Tests that the numpy gamma distribution has expected properties"""
    results = {}
    for target_cv in np.linspace(0.5, 3.0, num=3):
        for target_mean in np.linspace(.25, 2, num=4):
            result_key = f"{target_cv},{target_mean}"
            target_std = target_mean * target_cv
            target_variance = target_std ** 2
            shape = (target_mean ** 2) / target_variance
            scale = target_variance / target_mean
            generated_range = []
            for x in range(1000):
                generated_range.append(np.random.gamma(shape, scale))
            mean = np.mean(generated_range)
            std = np.std(generated_range)
            results[result_key] = (std/mean, mean)

    pass

def test_scalred_gamma_distribution_produces_expected_mean_and_cv():
    """Tests that the numpy gamma distribution has expected properties"""
    results = {}
    for target_cv in np.linspace(0.5, 3.0, num=3):
        target_mean = 1
        result_key = f"{target_cv}"
        target_std = target_mean * target_cv
        target_variance = target_std ** 2
        shape = (target_mean ** 2) / target_variance
        scale = target_variance / target_mean
        generated_range = []
        for x in range(50000):
            value = np.random.gamma(shape, scale)
            if value > 10:
                value = 10
            generated_range.append(value)
        max = np.max(generated_range)
        mean = np.mean(generated_range)
        std = np.std(generated_range)
        results[result_key] = (std/mean, mean, max)

    pass