"""
Runs the susceptibility variability study.

Modify the params variable to set the parameters of the study.

Parameters:

    pInfect:            Rate of infection
    pRemove:            Rate of removal
    pInfected:          Starting percent of population that is infected
    population:         Approximate population of the test.  Note: for certain network types (powerlaw cutoff) this
                        will only be approximate in order to maintain network statistical properties.
    time_scale:         Multiplier that converts model time units to days.
    days_to_run:        Cutoff number of days for model run.
    variability_method: Method with which to vary the susceptibility of individuals.  "constant", "gamma",
                        or "balanced_polynomial".
    variability_param1: First parameter for variability method.  For "balanced_polynomial", this is the exponent
                        to which a random fraction is raised.  For "gamma", this is the shape of the gamma function.
                        For "constant", this is the susceptibility that will be applied to all individuals.
    variability_param2: Second parameter for variability method.  For "gamma", this is the scale of the gamma function.
    intervention_1:     A string representing the first intervention.  The intervention will be applied from a start
                        day until an end day and have a certain percent chance per individual of cancelling an
                        infection.  The string should be formatted "{day_start}, {day_end}, {effectiveness}".
    intervention_2:     A string representing a second intervention.

"""
import epyc
import numpy as np
import matplotlib.pyplot as plt


from dataclasses import asdict

from covidsim.experiments.network_variability_study import NetworkVariabilityExperiment
from covidsim.datastructures import VariabilityStudyParams

# TODO: Add UI to set / save / reload parameters.
params = VariabilityStudyParams()
params.pInfect = 0.5
params.pRemove = 0.04
params.pInfected = 0.002
params.population = 5000
params.time_scale = .5
params.days_to_run = 350
params.randomize_network = True
params.network_type = 'powerlaw_cutoff'
params.network_param_1 = 2.0
params.network_param_2 = 100

params.variability_method = 'gamma'
params.variability_param_1 = 0.3
params.variability_param_2 = np.linspace(0.5, 3.0, num=7)

# params.intervention_1 = "18, 50, 0.5"
# params.intervention_2 = "100, 120, 0.1"

def my_func(x:float):
    return 2*(x**2) + x + 1

def derivative(f, x, d):
    return (f(x+d) - f(x)) / d

def main():
    xs = np.linspace(-8, 8, num=256)
    ys = []
    ds = []
    for x in xs:
        ys.append(my_func(x))

    ys = np.array(ys)

    d = 0.001
    for x in xs:
        ds.append(derivative(my_func, x, d))

    fig, ax = plt.subplots()
    plt.grid(which='both')
    plt.plot(xs, ys)
    plt.plot(xs, ds)

    plt.show()

if __name__ == "__main__":
    main()
