"""
Network variability study.

The purpose of this study is to examine how individual total susceptibility within a population varies depending
on network variability (how exposed an individual is to other nodes) vs. latent variability.

It does not run a simulation; it only creates networks and get metrics from them.
"""
import numpy as np

from covidsim.datastructures import VariabilityStudyParams
from covidsim.experiments.base_experiment import BaseExperiment


class NetworkVariabilityExperiment(BaseExperiment):

    def __init__(self, params: VariabilityStudyParams):

        super(NetworkVariabilityExperiment, self).__init__(params)

    def do(self, params, run_simulation: bool = False):
        res = super(NetworkVariabilityExperiment, self).do(params, run_simulation)

        # Gather custom results
        g = self._g

        res['population_size'] = len(g.nodes)

        # TODO: Move some of these metrics to a network class?
        res['graph_cov'] = np.std([x[1] for x in g.degree]) / np.mean([x[1] for x in g.degree])

        res['mean_individual_susceptibility'] = np.mean([g.nodes[x[0]]['susceptibility'] for x in g.degree])
        res['std_individual_susceptibility'] = np.std([g.nodes[x[0]]['susceptibility'] for x in g.degree])

        mean_exposure_susceptibility = np.mean(
            [1.0 - (1.0 - g.nodes[x[0]]['susceptibility']) ** x[1] for x in g.degree])
        std_exposure_susceptibility = np.std([1.0 - (1.0 - g.nodes[x[0]]['susceptibility']) ** x[1] for x in g.degree])

        coeff_of_variation = std_exposure_susceptibility / mean_exposure_susceptibility

        res['mean_exposure_susceptibility'] = mean_exposure_susceptibility
        res['std_exposure_susceptibility'] = std_exposure_susceptibility
        res['exposure_susceptibility_cov'] = coeff_of_variation
        res['individual_cov'] = res['std_individual_susceptibility'] / res['mean_individual_susceptibility']

        return res


