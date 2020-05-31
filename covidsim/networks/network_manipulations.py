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

    def __init__(self, params: StudyParams):
        self.params = params

    def setup_nodes(self, g):
        context = {}
        context['total_nodes'] = len(g.nodes)

        for index in g.nodes:
            node = g.nodes[index]
            node['infected'] = 0
            node['day_infected'] = -1
            context['index'] = index

            if 'variability_method' in asdict(self.params):
                if asdict(self.params)['variability_method'] == 'balanced_polynomial':
                    self._balanced_polynomial_susceptibility(node, context, self.params)

                if asdict(self.params)['variability_method'] == 'gamma':
                    self._gamma_susceptibility(node, context, self.params)

                if asdict(self.params)['variability_method'] == 'constant':
                    self._constant_susceptibility(node, context, self.params)

    @staticmethod
    def _balanced_polynomial_susceptibility(self, node, context, params: VariabilityStudyParams):
        """Raises random numbers (0 < num < 1) by an exponent, increasing the prevalence of low probabilities.
        These are balanced by taking a complement every other number.  The mean susceptibility will always tend
        towards 0.5."""

        if 'even_node' not in context:
            context['even_node'] = False

        if context['even_node']:
            node['susceptibility'] = 1.0 - random.random() ** params.variability_param_1
        else:
            node['susceptibility'] = random.random() ** params.variability_param_1

            context['even_node'] = not context['even_node']

    @staticmethod
    def _constant_susceptibility(self, node, context, params: VariabilityStudyParams):
        """Constant value susceptibility."""

        node['susceptibility'] = params.variability_param_1

    @staticmethod
    def _gamma_susceptibility(self, node, context, params: VariabilityStudyParams):
        """Assigns susceptibility based on a gamma function with parameters taken from the study params."""

        if 'gamma_susceptibilities' not in context:
            context['gamma_susceptibilities'] = [context['total_nodes']]
            context['max_gamma'] = -1
            for x in range(context['total_nodes']):
                context['gamma_susceptibility'][x] = np.random.gamma(params.variability_param_1,
                                                                     params.variability_param_2)
                if context['gamma_susceptibility'][x] > context['max_gamma']:
                    context['max_gamma'] = context['gamma_susceptibility'][x]

        node['susceptibility'] = context['gamma_susceptibilities'][context['index']]
