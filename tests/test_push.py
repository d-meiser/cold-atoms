from .context import coldatoms
import numpy as np

import unittest


class PushTestSuite(unittest.TestCase):
    """Test suite for particle pushes."""

    def test_zero_velocities(self):
        x = np.random.rand(3)
        v = np.zeros(3)
        x_old = x.copy()
        coldatoms.push(1.0, x, v)
        assert (x == x_old).all()

    def test_zero_accelerations(self):
        x = np.random.rand(3)
        v = np.random.rand(3)
        v_old = v.copy()
        coldatoms.push(1.0, x, v)
        assert (v == v_old).all()


if __name__ == '__main__':
    unittest.main()

