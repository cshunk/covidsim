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

from dataclasses import asdict

from covidsim.experiments.variability_study import VariabilityExperiment
from covidsim.datastructures import VariabilityStudyParams

# TODO: Add UI to set / save / reload parameters.
params = VariabilityStudyParams()
params.pInfect = 0.5
params.pRemove = 0.04
params.pInfected = 0.002
params.population = 5000
params.time_scale = .5
params.days_to_run = 350
params.variability_method = 'constant'
params.variability_param_1 = 0.058
params.variability_param_2 = 1


# params.intervention_1 = "18, 50, 0.5"
# params.intervention_2 = "100, 120, 0.1"

def main():
    e = VariabilityExperiment(params)

    # TODO: Add capability to save study file in user-specified location
    nb = epyc.JSONLabNotebook('variability-study.json')
    lab = epyc.Lab(nb)

    for key in asdict(params):
        lab[key] = asdict(params)[key]

    lab.runExperiment(epyc.RepeatedExperiment(e, 7))


if __name__ == "__main__":
    main()
