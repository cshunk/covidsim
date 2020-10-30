"""
Base class to be used for various common setup tasks
"""
import numpy as np
import networkx as nx
import pluggy

from dataclasses import asdict
from typing import Dict
from epydemic import *
from epyc import labnotebook

from covidsim.datastructures import SeriesRange, StudyParams
from covidsim.models.tracked_sir import TrackedSIR
from covidsim.networks.powerlaw_cutoff import make_powerlaw_with_cutoff, generate_from
from covidsim.networks.network_manipulations import NetworkInitialization

from covidsim.models import model_events


class BaseExperiment(StochasticDynamics):
    def __init__(self, params: StudyParams):

        if params.randomize_network:
            self._g = nx.erdos_renyi_graph(2, 1.0)  # Dummy graph
        else:
            self._g = self.generate_graph(params.network_type, params.population,
                                          params.network_param_1, params.network_param_2)
            NetworkInitialization(asdict(params)).setup_nodes(self._g)

        # Setup the plugin manager
        pm = pluggy.PluginManager("infectionmodel")
        pm.add_hookspecs(model_events)
        pm.load_setuptools_entrypoints("infectionmodel")

        self.plugins = pm

        # Create the model
        p = TrackedSIR(pm.hook)

        super(BaseExperiment, self).__init__(p, self._g)

    def do(self, params, run_simulation: bool = False):
        if params['randomize_network']:
            # Generate graph.
            self._g = self.generate_graph(params['network_type'], params['population'],
                                          params['network_param_1'], params['network_param_2'])
            NetworkInitialization(params).setup_nodes(self._g)

        res = {}
        if run_simulation:
            res = super(BaseExperiment, self).do(params)
        return res

    @staticmethod
    def generate_graph(network_type: str, population: int, param1: float, param2: float):
        """Generates a network according to the study parameters"""
        g = None
        if network_type == 'powerlaw_cutoff':
            g = generate_from(population,
                              make_powerlaw_with_cutoff(param1, param2))

        else:  # default to erdos_renyi
            kmean = param1  # mean node degree
            phi = (kmean + 0.0) / population  # probability of attachment between two nodes chosen at random

            g = nx.erdos_renyi_graph(population, phi)

        return g

    @staticmethod
    def aggregate_results(nb: labnotebook, params: StudyParams, series_to_smooth: Dict = {'daily_r': 5}):
        """Aggregates results across multiple experiments."""
        results = nb.resultsFor(asdict(params))

        aggregated_results = {}
        timeseries_results = {}

        for result in results:
            if result['metadata']['status']:
                for key in result['results']:
                    if type(result['results'][key]) is list:
                        if key in timeseries_results:
                            timeseries_results[key].append(result['results'][key][:params.days_to_run])
                        else:
                            timeseries_results[key] = [result['results'][key][:params.days_to_run]]

        for key in timeseries_results:
            aggregated_results[key] = SeriesRange(None, None, None).create_from_list(
                timeseries_results[key],
                expected_length=params.days_to_run,
                smoothing=(series_to_smooth[key] if key in series_to_smooth else 0))

        # TODO: Is this part necessary?  Maybe just use built in dataframe method instead?
        for result in [x['results'] for x in results if x['metadata']['status']][:1]:
            for key in result:
                if not type(result[key]) is list:
                    aggregated_results[key] = np.mean([x['results'][key] for x in results if x['metadata']['status']])

        return aggregated_results
