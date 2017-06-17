import coldatoms
import numpy as np


class test_rng(object):

    def setup(self):
        self.rng = coldatoms.Rng()

    def test_construct_rng(self):
        pass

    def test_get_random_number(self):
        nums = 2.0 * np.ones(10)
        self.rng.fill(nums)
        for a in nums:
            assert(a >= 0.0 and a < 1.0)
        assert(np.std(nums) > 1.0e-9)

