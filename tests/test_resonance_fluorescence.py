from .context import coldatoms
import numpy as np

speed_of_light = 3.0e8
wavelength = 1.0e-6
k = np.array([2.0 * np.pi / wavelength, 0.0, 0.0])


class ConstantIntensity(object):
    def __init__(self, intensity):
        self.intensity = intensity

    def __evaluate__(self, x):
        return np.full(x.shape, self.intensity)


class ConstantDetuning(object):
    def __init__(self, detuning):
        self.detuning = detuning

    def __evaluate__(self, x, v):
        return np.full(x.shape, self.detuning)


def test_can_create_resonance_fluorescence():
    intensity = ConstantIntensity(0.1)
    detuning = ConstantDetuning(0.0)
    fluorescence = coldatoms.RadiationPressure(1.0e8, k, intensity, detuning)

