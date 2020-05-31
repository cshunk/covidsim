"""
Module contains the TrackedSIR model.

This model operates on a provided network.  Various standard daily data points are tracked as epidemic events occur.

The model can be customized by the use of parameters, and also the application of various plugins.
"""
import random
import numpy as np

from epydemic import *


class TrackedSIR(CompartmentedModel):
    SUSCEPTIBLE = 'S'
    INFECTED = 'I'
    REMOVED = 'R'

    P_INFECTED = 'pInfected'
    P_INFECT = 'pInfect'
    P_REMOVE = 'pRemove'

    SI = 'SI'

    def __init__(self, hook):
        super(TrackedSIR, self).__init__()
        self.timeseries_results = dict()
        self.interventions = dict()
        self.params = None
        self.hook = hook

    # Overriden methods
    def build(self, params):
        """Executes once before the simulation starts.  Initializes compartments and reporting variables."""
        self.params = params

        self.timeseries_results['daily_infections'] = []
        self.timeseries_results['currently_infected'] = []

        self.addCompartment(self.INFECTED, params['pInfected'])
        self.addCompartment(self.REMOVED, 0.0)
        self.addCompartment(self.SUSCEPTIBLE, 1 - params['pInfected'])

        self.trackNodesInCompartment(self.INFECTED)
        self.trackEdgesBetweenCompartments(self.SUSCEPTIBLE, self.INFECTED, name=self.SI)

        if 'always_infect' in params and params['always_infect']:
            self.addEventPerElement(self.SI, 1.0, self.infect)
        else:
            self.addEventPerElement(self.SI, params['pInfect'], self.infect)

        self.addEventPerElement(self.INFECTED, params['pRemove'], self.remove)

    def infect(self, t, e):
        """Infect event.  May be cancelled by an intervention at a certain probability."""
        (n, m) = e
        infecting_node = self._g.nodes[m]
        exposed_node = self._g.nodes[n]
        day = int(t * self.params['time_scale'])

        # Apply effects of interventions
        if self._intervention_cancels_infection(day, e):
            return

        # Use individual susceptibility if applicable
        if 'susceptibility' in exposed_node and random.random() > exposed_node['susceptibility']:
            return

        # increment various infection counters
        if 'day_infected' not in infecting_node:
            infecting_node['day_infected'] = 0

        if 'infecting_days' not in infecting_node:
            infecting_node['infected'] = 0
            infecting_node['infecting_days'] = {}
        infecting_node['infected'] += 1
        infecting_node['infecting_days'][infecting_node['infected']] = day

        exposed_node['day_infected'] = day

        di = self.timeseries_results['daily_infections']
        ci = self.timeseries_results['currently_infected']

        while len(di) - 1 < day:
            di.append(0)
        di[day] += 1

        if len(ci) == 0:
            num_infected = len(
                [self._g.nodes[x] for x in self._g.nodes if self._g.nodes[x]['compartment'] == self.INFECTED])
            ci.append(num_infected)

        while len(ci) - 1 < day:
            ci.append(ci[-1])
        ci[day] += 1

        # Finally, do the actual compartment change
        self.changeCompartment(n, self.INFECTED)
        self.markOccupied(e, t)

        self.hook.track_infection_event(infecting_node=infecting_node, exposed_node=exposed_node, day=day,
                                        results=self.timeseries_results, graph=self._g)

    def remove(self, t, n):
        """Remove event"""
        day = int(t * self.params['time_scale'])

        # Record days_infected and decrement currently infected counter
        node = self._g.nodes[n]
        node['days_infected'] = day - node['day_infected']

        ci = self.timeseries_results['currently_infected']
        if len(ci) == 0:
            num_infected = len(
                [self._g.nodes[x] for x in self._g.nodes if self._g.nodes[x]['compartment'] == self.INFECTED])
            ci.append(num_infected)

        while len(ci) - 1 < day:
            ci.append(ci[-1])

        ci[day] -= 1

        # Do actual compartment change
        self.changeCompartment(n, self.REMOVED)

        self.hook.track_remove_event(removed_node=node, day=day, results=self.timeseries_results, graph=self._g)

    def results(self):
        """Collects and returns results after the simulation has ended."""
        res = super(TrackedSIR, self).results()

        self.hook.finalize_results(initial_results=self.timeseries_results, final_results=res, params=self.params)

        # TODO: Fix this dependency issue
        di = res['daily_infections']
        ci = res['currently_infected']

        # Calculate the average length of an infection
        n = self._g.nodes
        mil = np.mean([n[x]['days_infected'] for x in n if 'days_infected' in n[x]])
        res['mean_infection_length'] = mil

        res['daily_r'] = [((di[x + 1] / ci[x]) if ci[x] != 0 else 0) * mil for x in range(len(ci) - 1)]

        return res

    def reset(self):
        """Runs after a single simulation, prepares for the next simulation."""
        super(TrackedSIR, self).reset()
        self.timeseries_results = dict()

    # --Private methods--

    def _intervention_cancels_infection(self, day, e):
        """Cancels an intervention at a certain specified probability based on the intervention parameters."""
        (n, m) = e

        i = 1
        while 'intervention_' + str(i) in self.params and self.params['intervention_' + str(i)] is not None:
            intervention = self.params['intervention_' + str(i)].split(',')
            if int(intervention[0]) <= day <= int(intervention[1]):
                if random.random() < float(intervention[2]):
                    return True
            i += 1
        return False
