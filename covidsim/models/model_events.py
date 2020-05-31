"""
Standard events for the epydemic models.

Event specifications are defined using the pluggy @hookspec decorator.

Event implementations are contained in classes and defined using the pluggy @hookimp decorator.
"""

import pluggy
import covidsim.models

hookspec = pluggy.HookspecMarker("infectionmodel")


@hookspec
def track_infection_event(infecting_node, exposed_node, day, results, graph):
    """
    Fires after an infection occurs

    :param infecting_node: Node that has just spread the infection
    :param exposed_node: Node that has just become infected
    :param day: Integer day of infection run
    :param results: Results collection object
    :param graph: Optional graph for the model
    :return:
    """


@hookspec
def track_remove_event(removed_node, day, results, graph):
    """
    Fires after a remove occurs

    :param removed_node: Node that has just removed
    :param day: Integer day of infection run
    :param results: Results collection object
    :param graph: Optional graph for the model
    :return:
    """


@hookspec
def finalize_results(initial_results, final_results, params):
    """
    Fires after run is complete

    :param initial_results: Collection containing data
    :param final_results: Collection in which to contain final data results
    :param params: Run parameters that may affect the finalization
    :return:
    """


# Built-in trackers
class InfectionsAndInfectedTracker:
    """Tracks daily infections and daily currently infected."""

    @staticmethod
    @covidsim.models.hookimpl
    def finalize_results(initial_results, final_results, params):
        di = initial_results['daily_infections']
        ci = initial_results['currently_infected']

        if len(di) < params['days_to_run']:
            di += [0] * (params['days_to_run'] - len(di))
        if len(di) > params['days_to_run']:
            di = di[:params['days_to_run']]

        if len(ci) < params['days_to_run']:
            ci += [0] * (params['days_to_run'] - len(ci))
        if len(ci) > params['days_to_run']:
            ci = ci[:params['days_to_run']]

        final_results['daily_infections'] = di
        final_results['currently_infected'] = ci


class SusceptibleInfectionsTracker:
    """Tracks how susceptible on average were all individuals who became infected per day."""

    @staticmethod
    @covidsim.models.hookimpl
    def track_infection_event(infecting_node, exposed_node, day, results, graph):
        if 'daily_susceptible_infections' not in results:
            results['daily_susceptible_infections'] = [[0, 0]] * (day + 1)

        while len(results['daily_susceptible_infections']) < day + 1:
            results['daily_susceptible_infections'] += [[0, 0]]

        results['daily_susceptible_infections'][day][0] += exposed_node['susceptibility']
        results['daily_susceptible_infections'][day][1] += 1

    @staticmethod
    @covidsim.models.hookimpl
    def finalize_results(initial_results, final_results, params):
        si = initial_results['daily_susceptible_infections']
        if len(si) < params['days_to_run']:
            si += [[0, 0]] * (params['days_to_run'] - len(si))
        if len(si) > params['days_to_run']:
            si = si[:params['days_to_run']]

        final_results['daily_susceptible_infections'] = [x[0] / x[1] if x[1] > 0 else 0 for x in si]
