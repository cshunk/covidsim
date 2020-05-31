"""
Runs the report for the variability study.

It uses the same parameters defined in variability_study_run.py.
"""
import epyc
import matplotlib.pyplot as plt
import numpy as np

from dataclasses import asdict

from covidsim.experiments.variability_study import VariabilityExperiment, get_graphic_summary_data
from covidsim.datastructures import VariabilityStudyParams
from covidsim.utils.graph_utils import plot_series_range, ColorSchemes
from scripts.variability_study_run import params


def main():
    nb = epyc.JSONLabNotebook('variability-study.json')

    errors = 0
    successful = 0
    for result in nb.resultsFor(asdict(params)):
        if result['metadata']['status']:
            successful += 1
        else:
            errors += 1

    if errors > 0:
        print(f'Found {errors} invalid results with exception messages.')

    if successful == 0:
        print(f'Found no successful experiment results for those parameters.  Exiting.')
        return

    res = get_graphic_summary_data(nb, params)

    fig, ax = plt.subplots()
    plt.grid(which='both')

    # Daily infections
    plot_series_range(res['daily_infections'], plt, ax, 'Infections per day', ColorSchemes().blue)

    # Daily currently infected
    # ax2 = ax.twinx()
    # plot_series_range(res['daily_infected'], plt, ax2, None, ColorSchemes().green)

    # R
    ax3 = ax.twinx()
    major_ticks = np.arange(0, 10, 0.5)
    ax3.set_yticks(major_ticks)
    ax3.set_ylim([0, 10])
    plot_series_range(res['daily_r'], plt, ax3, 'R', ColorSchemes().red)

    # Tracked scalar results
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    plt.text(0.5, 0.75,
             f"Exposure/Susceptibility CoV: {res['exposure_susceptibility_cov']:10.3f}\n"
             + f"Exposure/Susceptibility Mean: {res['mean_exposure_susceptibility']:10.3f}\n"
             + f"Network CoV: {res['graph_cov']:10.3f}\n"

             + f"Susceptibility mean: {res['mean_individual_susceptibility']:10.3f}\n"
             + f"Susceptibility CoV: {res['individual_cov']:10.3f}\n"

             + f"Percent for Herd Immunity: {res['infections_for_herd_immunity_pct'] * 100:10.1f}\n"
             + f"Total Population Infected: %{res['total_infected_pct'] * 100:10.1f}\n"
             + f"Infectious Period: {res['mean_infection_length']:10.1f}",
             transform=ax.transAxes, bbox=props)

    # Significant value markers
    color = 'black'
    plt.axhline(y=1.0, linestyle=':', color=color)
    plt.axvline(x=res['r_equals_1_threshold'], linestyle=':', color=color)

    plt.show()


if __name__ == "__main__":
    main()
