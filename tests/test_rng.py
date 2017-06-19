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

    def test_reseeding_gives_same_sequence(self):
        nums = 2.0 * np.ones(10)
        seed = 1234
        self.rng.seed(seed)
        self.rng.fill(nums)
        self.rng.seed(seed)
        more_nums = np.zeros_like(nums)
        self.rng.fill(more_nums)
        assert(np.all(nums == more_nums))

    def test_new_numbers_are_produced(self):
        nums = 2.0 * np.ones(10)
        self.rng.fill(nums)
        more_nums = np.zeros_like(nums)
        self.rng.fill(more_nums)
        assert(np.all(nums != more_nums))

    def test_gaussian(self):
        nums = 2.0 * np.ones(10000)
        mean = 12.3
        std = 3.4
        self.rng.fill_gaussian(mean, std, nums)
        assert(np.abs((np.mean(nums) - mean) / mean) < 0.1)
        assert(np.abs((np.std(nums) - std) / std) < 0.1)
