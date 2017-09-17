import numpy as np
import coldatoms_lib


def _harmonic_trap_forces_ref(positions, q, kx, ky, kz, phi, dt, f):
    cphi = np.cos(phi)
    sphi = np.sin(phi)

    x = positions[:, 0]
    y = positions[:, 1]
    z = positions[:, 2]

    f[:, 0] += dt * q * (
        (-kx * cphi * cphi - ky * sphi * sphi) * x + cphi * sphi * (ky - kx) * y)
    f[:, 1] += dt * q * (
        cphi * sphi * (ky - kx) * x + (-kx * sphi * sphi - ky * cphi * cphi) * y)
    f[:, 2] += -dt * q * kz * z


class HarmonicTrapPotential(object):
    def __init__(self, kx, ky, kz):
        self.kx = kx
        self.ky = ky
        self.kz = kz
        self.phi = 0.0
        self._harmonic_trap_forces = coldatoms_lib.harmonic_trap_forces
        self._harmonic_trap_forces_per_particle_charges = coldatoms_lib.harmonic_trap_forces_per_particle_charge

    def use_reference_implementations(self):
        self._harmonic_trap_forces = _harmonic_trap_forces_ref
        self._harmonic_trap_forces_per_particle_charges = _harmonic_trap_forces_ref

    def force(self, dt, ensemble, f):
        positions = ensemble.x
        if 'charge' in ensemble.ensemble_properties:
            q = ensemble.ensemble_properties['charge']
            self._harmonic_trap_forces(positions, q, self.kx, self.ky, self.kz,
                self.phi, dt, f)
        elif 'charge' in ensemble.particle_properties:
            q = ensemble.particle_properties['charge']
            self._harmonic_trap_forces_per_particle_charges(
                positions, q, self.kx, self.ky, self.kz, self.phi, dt, f)
        else:
            raise RuntimeError('Must provide a charge to compute coulomb force')
