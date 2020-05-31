"""
This module contains various project shared datastructures.
"""
import numpy as np

from dataclasses import dataclass
from typing import List

@dataclass
class Intervention:
    start_day: int
    end_day: int
    percent_reduction: float

@dataclass
class StudyParams:
    # Standard compartments
    pRemove: float = 0.002
    pInfect: float = 0.5
    pInfected: float = 0.01

    # Network parameters
    population: int = 5000
    network_param_1: float = 2.0
    network_param_2: float = 10.0

    # Time parameters
    days_to_run: int = 350
    time_scale: float = 10.0

    # Interventions
    intervention_1: str = None
    intervention_2: str = None

@dataclass
class VariabilityStudyParams(StudyParams):
    variability_method: str = 'balanced_polynomial'
    variability_param_1: float = 3.0
    variability_param_2: float = 3.0
    always_infect: bool = True

@dataclass
class SeriesRange:
    """Combines multiple data series, usually from separate runs of a simulation, into a mean, a low and a high.
    The low and the high are one STD from the mean."""
    mean: List[float]
    high: List[float]
    low: List[float]

    def create_from_list(self, data: List[List], expected_length: int = 0):

        if expected_length > 0:
            for dat_list in data:
                if len(dat_list) < expected_length:
                    dat_list += [0] * (expected_length - len(dat_list))

        self.mean = np.mean(data, axis=0)
        std = np.std(data, axis=0)
        self.high = self.mean + std
        self.low = self.mean - std

        return self

