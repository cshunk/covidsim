"""
Runs the report for the network variability study.

It uses the same parameters defined in network_variability_study_run.py.
"""
import epyc
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np

from dataclasses import asdict

from covidsim.utils.graph_utils import plot_series_range, ColorSchemes
from scripts.network_variability_study_run import params


def main():
    nb = epyc.JSONLabNotebook('network-variability-study.json')

    df = nb.dataframe()

    fig = plt.figure(figsize=(8, 8))
    ax = fig.gca(projection='3d')

    plt_result = 'exposure_susceptibility_cov'
    x = 'mean_individual_susceptibility'
    y = 'individual_cov'

    ax.scatter(df[x], df[y], df[plt_result],
               c=df[plt_result], depthshade=False, cmap=cm.coolwarm)
    ax.set_xlim(np.floor(df[x].min()), np.ceil(df[x].max()))
    ax.set_ylim(np.floor(df[y].min()), np.ceil(df[y].max()))
    ax.set_zlim(np.floor(df[plt_result].min()), np.ceil(df[plt_result].max()))

    plt.show()


if __name__ == "__main__":
    main()
