"""
This module contains various methods for the purpose of applying manipulations to the population network,
either before or during a simulation.
"""
import random
import numpy as np

from dataclasses import asdict

from covidsim.datastructures import StudyParams, VariabilityStudyParams


class NetworkInitialization:
    """Initializes all of the nodes of the network.  Based on the parameters
    of the specific study.  TODO: Make this a plugin structure"""

    def __init__(self, params):
        self.params = params

    def setup_nodes(self, g):
        context = {}
        context['total_nodes'] = len(g.nodes)

        index = 0
        for node_num in g.nodes:
            node = g.nodes[node_num]
            node['infected'] = 0
            node['day_infected'] = -1
            context['index'] = index
            context['node'] = node
            index += 1

            if 'variability_method' in self.params:
                if self.params['variability_method'] == 'balanced_polynomial':
                    self._balanced_polynomial_susceptibility(node, context, self.params['variability_param_1'])

                if self.params['variability_method'] == 'gamma':
                    self._gamma_susceptibility(node, self.params['variability_param_1'], self.params['variability_param_2'])

                if self.params['variability_method'] == 'constant':
                    self._constant_susceptibility(node, context,
                                                  self.params['variability_param_1'],
                                                  self.params['variability_param_2'])

    @staticmethod
    def _balanced_polynomial_susceptibility(node, context, exponent: float):
        """Raises random numbers (0 < num < 1) by an exponent, increasing the prevalence of low probabilities.
        These are balanced by taking a complement every other number.  The mean susceptibility will always tend
        towards 0.5."""

        if 'even_node' not in context:
            context['even_node'] = False

        if context['even_node']:
            node['susceptibility'] = 1.0 - random.random() ** exponent
        else:
            node['susceptibility'] = random.random() ** exponent

            context['even_node'] = not context['even_node']

    @staticmethod
    def _constant_susceptibility(node, context, susceptibility: float):
        """Constant value susceptibility."""

        node['susceptibility'] = susceptibility

    @staticmethod
    def _gamma_susceptibility(node, target_mean: float, target_cv: float):
        """Assigns susceptibility based on a gamma function with parameters taken from the study params."""
        target_std = target_mean * target_cv
        target_variance = target_std ** 2
        shape = (target_mean ** 2) / target_variance
        scale = target_variance / target_mean
        node['susceptibility'] = np.random.gamma(shape, scale)
        # if node['susceptibility'] > 1.0:
        #     node['susceptibility'] = 1.0
