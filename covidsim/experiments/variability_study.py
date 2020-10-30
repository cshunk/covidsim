"""
Susceptibility variability study.

The purpose of this study is to examine how the herd immunity threshold is effected by variation in individual
susceptibility to infection by a virus.  That variations in exposure or susceptibility could have substantial
effects on the herd immunity threshold was proposed in this paper:

https://www.medrxiv.org/content/10.1101/2020.04.27.20081893v1.full.pdf

It was tested only by a simplistic differential equation based SEIR model.  This experiment proposes to test the
hypothesis on a simulation using a heterogeneous network to simulate an epidemic population with a variable exposure.
The model nodes are also assigned a variety of individual susceptibility values (representing probability of infection
when exposed to another infected node).

We can therefore vary exposure-based susceptibility and individual susceptibility (representing, one presumes, the
latent immune system strength of an individual) and see how the herd immunity reacts.
"""
import numpy as np

from typing import Dict
from epyc import labnotebook

from covidsim.models import model_events
from covidsim.datastructures import VariabilityStudyParams

from covidsim.experiments.network_variability_study import NetworkVariabilityExperiment


class VariabilityExperiment(NetworkVariabilityExperiment):

    def __init__(self, params: VariabilityStudyParams):

        super(VariabilityExperiment, self).__init__(params)

        self.plugins.register(model_events.SusceptibleInfectionsTracker)
        self.plugins.register(model_events.InfectionsAndInfectedTracker)

    def do(self, params):
        res = super(VariabilityExperiment, self).do(params, run_simulation=True)

        # Gather custom results
        g = self._g

        res['total_infected'] = res['I'] + res['R']
        res['total_infected_pct'] = res['total_infected'] / res['population_size']

        return res

    @staticmethod
    def aggregate_results(nb: labnotebook, params: VariabilityStudyParams, series_to_smooth: Dict = {'daily_r': 5}):
        res = super(VariabilityExperiment, VariabilityExperiment).aggregate_results(nb, params, series_to_smooth)

        # Get the point at which R drops below 1
        r_less_than_one = 0
        while res['daily_r'].mean[r_less_than_one] > 1:
            r_less_than_one += 1

        infections_for_herd_immunity_pct = np.sum(res['daily_infections'].mean[:r_less_than_one]) / res['population_size']

        res['infections_for_herd_immunity_pct'] = infections_for_herd_immunity_pct
        res['r_equals_1_threshold'] = r_less_than_one

        return res
