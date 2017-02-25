from .context import coldatoms
import numpy as np

speed_of_light = 3.0e8
wavelength = 1.0e-6
hbar_k = 1.0e-34 * np.array([2.0 * np.pi / wavelength, 0.0, 0.0])


class ConstantIntensity(object):
    def __init__(self, intensity):
        self.intensity = intensity

    def intensities(self, x):
        return np.full(x.shape[0], self.intensity)


class ConstantDetuning(object):
    def __init__(self, detuning):
        self.detuning = detuning

    def detunings(self, x, v):
        return np.full(x.shape[0], self.detuning)


intensity = ConstantIntensity(0.1)
detuning = ConstantDetuning(0.0)


def test_can_create_resonance_fluorescence():
    fluorescence = coldatoms.RadiationPressure(1.0e8,
                                               hbar_k, intensity, detuning)


def test_force_is_non_zero():
    fluorescence = coldatoms.RadiationPressure(1.0e8,
                                               hbar_k, intensity, detuning)
    ensemble = coldatoms.Ensemble()
    # In one millisecond we expect to scatter more than one photon
    f = fluorescence.force(1.0e-3, ensemble)
    assert(np.linalg.norm(f) > np.linalg.norm(hbar_k))


def test_force_is_not_unreasonably_large():
    fluorescence = coldatoms.RadiationPressure(1.0e8,
                                               hbar_k, intensity, detuning)
    ensemble = coldatoms.Ensemble()
    # In one millisecond we expect to scatter no more than s * (gamma/2pi)* dt
    # photons.
    expected_number_of_recoils = (intensity.intensity *
                                  (1.0e8 / 2.0 / np.pi) * 1.0e-3)
    print('expected_number_of_recoils == ', expected_number_of_recoils)
    f = fluorescence.force(1.0e-3, ensemble)
    print(f)
    print(expected_number_of_recoils * np.linalg.norm(hbar_k))
    assert(np.linalg.norm(f) <
           3.0 * expected_number_of_recoils * np.linalg.norm(hbar_k))
