"""
This code is taken from the epydemic advanced tutorial.

It creates a network with a powerlaw distribution of connectivity, cutoff at a certain maximum node degree.
"""
import networkx as nx
import math
import numpy as np
from mpmath import polylog as Li   # use standard name


def make_powerlaw_with_cutoff(alpha, kappa ):
    '''Create a model function for a powerlaw distribution with exponential cutoff.

    :param alpha: the exponent of the distribution
    :param kappa: the degree cutoff
    :returns: a model function'''
    C = Li(alpha, math.exp(-1.0 / kappa))
    def p( k ):
        return (pow((k + 0.0), -alpha) * math.exp(-(k + 0.0) / kappa)) / C
    return p


def generate_from(N, p, maxdeg = 100 ):
    '''Generate a random graph with degree distribution described
    by a model function.

    :param N: number of numbers to generate
    :param p: model function
    :param maxdeg: maximum node degree we'll consider (defaults to 100)
    :returns: a network with the given degree distribution'''

    # construct degrees according to the distribution given
    # by the model function
    ns = []
    t = 0
    for i in range(N):
        while True:
            k = 1 + int (np.random.random() * (maxdeg - 1))
            if np.random.random() < p(k):
                ns = ns + [ k ]
                t = t + k
                break

    # if the sequence is odd, choose a random element
    # and increment it by 1 (this doesn't change the
    # distribution significantly, and so is safe)
    if t % 2 != 0:
        i = int(np.random.random() * len(ns))
        ns[i] = ns[i] + 1

    # populate the network using the configuration
    # model with the given degree distribution
    g = nx.configuration_model(ns, create_using = nx.Graph())
    g = g.subgraph(max(nx.connected_components(g), key = len)).copy()
    g.remove_edges_from(list(nx.selfloop_edges(g)))
    return g