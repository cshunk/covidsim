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
import pluggy

from dataclasses import asdict
from epydemic import *

from covidsim.datastructures import SeriesRange
from covidsim.models.tracked_sir import TrackedSIR
from covidsim.networks.powerlaw_cutoff import make_powerlaw_with_cutoff, generate_from
from covidsim.networks.network_manipulations import NetworkInitialization
from covidsim.datastructures import VariabilityStudyParams

from covidsim.models import model_events


class VariabilityExperiment(StochasticDynamics):
    def __init__(self, params: VariabilityStudyParams):

        g = generate_from(params.population,
                          make_powerlaw_with_cutoff(params.network_param_1, params.network_param_2))

        NetworkInitialization(params).setup_nodes(g)

        self._g = g

        pm = pluggy.PluginManager("infectionmodel")
        pm.add_hookspecs(model_events)
        pm.load_setuptools_entrypoints("infectionmodel")
        pm.register(model_events.SusceptibleInfectionsTracker)
        pm.register(model_events.InfectionsAndInfectedTracker)

        p = TrackedSIR(pm.hook)

        super(VariabilityExperiment, self).__init__(p, g)


    def do(self, params):
        res = super(VariabilityExperiment, self).do(params)

        # Gather custom results
        g = self._g

        res['population_size'] = res['S'] + res['I'] + res['R']
        res['total_infected'] = res['I'] + res['R']
        res['total_infected_pct'] = res['total_infected'] / res['population_size']

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


def get_graphic_summary_data(nb, params: VariabilityStudyParams):

    res = nb.resultsFor(asdict(params))

    # Timeseries results
    all_infections = []
    all_infected = []
    all_r_values = []

    for result in nb.resultsFor(asdict(params)):
        if result['metadata']['status']:
            all_infections.append(result['results']['daily_infections'][:params.days_to_run])
            all_infected.append(result['results']['currently_infected'][:params.days_to_run])
            all_r_values.append(result['results']['daily_r'][:params.days_to_run + 2])

    daily_infections = SeriesRange(None,None,None).create_from_list(all_infections, expected_length=params.days_to_run)
    daily_r = SeriesRange(None,None,None).create_from_list(all_r_values, expected_length=params.days_to_run)
    daily_infected = SeriesRange(None, None, None).create_from_list(all_infected, expected_length=params.days_to_run)

    # Calculate a smoothed R timeline
    r_cumsum = np.cumsum(np.insert(daily_r.mean, 0, 0))
    M = 5
    daily_r.mean = ((r_cumsum[M:] - r_cumsum[:-M]) / float(M))
    if len(daily_r.mean) < params.days_to_run:
        daily_r.mean = np.append(daily_r.mean, [0]*(len(daily_r.mean - params.days_to_run)))
    if len(daily_r.mean) > params.days_to_run:
        daily_r.mean = daily_r.mean[:params.days_to_run]
    daily_r.high = daily_r.high[:params.days_to_run]
    daily_r.low = daily_r.low[:params.days_to_run]

    # Get the point at which R drops below 1
    r_less_than_one = 0
    while daily_r.mean[r_less_than_one] > 1:
        r_less_than_one += 1

    mean_population = np.mean([x['results']['population_size'] for x in res if x['metadata']['status']])
    infections_for_herd_immunity_pct = np.sum(daily_infections.mean[:r_less_than_one]) / mean_population

    results = {
        'infections_for_herd_immunity_pct': infections_for_herd_immunity_pct,
        'daily_infections': daily_infections,
        'daily_infected': daily_infected,
        'daily_r': daily_r,
        'r_equals_1_threshold': r_less_than_one
    }

    # Single value results
    for res_name in ['total_infected_pct', 'graph_cov', 'mean_individual_susceptibility', 'individual_cov',
                     'mean_exposure_susceptibility', 'exposure_susceptibility_cov', 'mean_infection_length']:
        results[res_name] = np.mean([x['results'][res_name] for x in res if x['metadata']['status']])

    return results
