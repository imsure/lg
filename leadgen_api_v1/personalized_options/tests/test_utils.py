import unittest

from .. import utils

class TestUtilsMethods(unittest.TestCase):

    def test_unique_place_id(self):
        place_id_iter = utils.unique_place_id()
        self.assertEqual(next(place_id_iter), 1)
        self.assertEqual(next(place_id_iter), 2)
        self.assertEqual(next(place_id_iter), 3)

    def test_probability_list(self):
        prob_list = utils.probability_list()
        self.assertEqual(len(prob_list), 96)
        self.assertAlmostEqual(sum(prob_list), 100.0)
