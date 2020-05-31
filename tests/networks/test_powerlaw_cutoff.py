"""
Module contains tests just for the powerlaw cutoff network functions.
"""
import pytest

from covidsim.networks.powerlaw_cutoff import make_powerlaw_with_cutoff, generate_from

@pytest.fixture
def powerlaw_cutoff_network(population: int = 100):

    return generate_from(population, make_powerlaw_with_cutoff(2, 10))
