"""
Module contains tests specifically for the TrackedSIR class.
"""
import pytest

from dataclasses import asdict

from covidsim.models.tracked_sir import TrackedSIR
from covidsim.datastructures import StudyParams


@pytest.fixture
def standard_params() -> StudyParams:
    return StudyParams(population=1000, pInfected=0.1)


@pytest.fixture
def model(powerlaw_cutoff_network, standard_params) -> TrackedSIR:

    model = TrackedSIR()
    model._g = powerlaw_cutoff_network
    model.build(standard_params)

    model.setUp(asdict(standard_params))

    return model


def test_infect_increases_infections(model: TrackedSIR):
    """Infect method increases infections when invoked directly."""
    day = 1
    i1 = model.results()['I']

    for e in list(model._g.edges)[:50]:
        model.infect(day, e)
        day += 1

    i2 = model.results()['I']

    assert i2 > i1

