from itertools import product
from astropy import units as u, constants as const
import numpy as np
from ..nuclear import (nuclear_binding_energy, nuclear_reaction_energy)

import pytest


def test_nuclear_binding_energy():
    assert nuclear_binding_energy('p') == 0
    assert nuclear_binding_energy('n') == 0
    assert nuclear_binding_energy('He-4') == nuclear_binding_energy('alpha') \
        == nuclear_binding_energy('He', 4)


def test_nuclear_binding_energy_D_T():
    before = nuclear_binding_energy("D") + nuclear_binding_energy("T")
    after = nuclear_binding_energy("alpha")
    E_in_MeV = (after - before).to(u.MeV).value  # D + T --> alpha + n + E
    assert np.isclose(E_in_MeV, 17.58, rtol=0.01)


# (argument, expected_error)
nuclear_binding_energy_table = [
    ("H", ValueError),
    (1.1, TypeError)]


@pytest.mark.parametrize("argument, expected_error",
                         nuclear_binding_energy_table)
def test_nuclear_binding_energy_error(argument, expected_error):
    with pytest.raises(expected_error):
        nuclear_binding_energy(argument)


def test_nuclear_reaction_energy():
    reaction1 = 'D + T --> alpha + n'
    reaction2 = 'T + D -> n + alpha'
    released_energy1 = nuclear_reaction_energy(reaction1)
    released_energy2 = nuclear_reaction_energy(reaction2)
    assert np.isclose((released_energy1.to(u.MeV)).value, 17.58, rtol=0.01)
    assert released_energy1 == released_energy2


def test_nuclear_reaction_energy_triple_alpha():
    triple_alpha1 = 'alpha + He-4 --> Be-8'
    triple_alpha2 = 'Be-8 + alpha --> carbon-12'
    energy_triplealpha1 = nuclear_reaction_energy(triple_alpha1)
    energy_triplealpha2 = nuclear_reaction_energy(triple_alpha2)
    assert np.isclose(energy_triplealpha1.to(u.keV).value, -91.8, atol=0.1)
    assert np.isclose(energy_triplealpha2.to(u.MeV).value, 7.367, atol=0.1)

    reactants = ['He-4', 'alpha']
    products = ['Be-8']
    energy = nuclear_reaction_energy(reactants=reactants, products=products)
    assert np.isclose(energy.to(u.keV).value, -91.8, atol=0.1)


def test_nuclear_reaction_energy_alpha_decay():
    alpha_decay_example = 'U-238 --> Th-234 + alpha'
    energy_alpha_decay = nuclear_reaction_energy(alpha_decay_example)
    assert np.isclose(energy_alpha_decay.to(u.MeV).value, 4.26975, atol=1e-5)


def test_nuclear_reaction_energy_triple_alpha_r():
    triple_alpha1_r = '4He-4 --> 2Be-8'
    energy_triplealpha1_r = nuclear_reaction_energy(triple_alpha1_r)
    assert np.isclose(energy_triplealpha1_r.to(u.keV).value,
                      -91.8 * 2, atol=0.1)


def test_nuclear_reaction_energy_beta():
    energy1 = nuclear_reaction_energy(reactants=['n'], products=['p', 'e-'])
    assert np.isclose(energy1.to(u.MeV).value, 0.78, atol=0.01)
    energy2 = nuclear_reaction_energy(
        reactants=['Mg-23'], products=['Na-23', 'e+'])
    assert np.isclose(energy2.to(u.MeV).value, 3.034591, atol=1e-5)


# (reaction, kwargs, expected_error)
nuclear_reaction_energy_error_table = [
    ('H + H --> H', {}, ValueError),
    (1, {}, TypeError),
    ('H-1 + H-1 --> H-1', {}, ValueError),
    ("invalid input", {}, ValueError),
    ('p --> n', {}, ValueError),
    ('p --> p', {'reactants': ['p'], 'products': ['p']}, ValueError),
]


@pytest.mark.parametrize(
    "reaction, kwargs, expected_error", nuclear_reaction_energy_error_table)
def test_nuclear_reaction_energy_error(reaction, kwargs, expected_error):
    with pytest.raises(expected_error):
        nuclear_reaction_energy(reaction, **kwargs)
