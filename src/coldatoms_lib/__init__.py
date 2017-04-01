import pyximport
pyximport.install()

from .coldatoms_lib import(
    coulomb_force,
    coulomb_force_per_particle_charge
    )

