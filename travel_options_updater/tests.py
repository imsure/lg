import unittest
import constants as const
import utils


class TestConstants(unittest.TestCase):

    def test_slot2time(self):
        self.assertEqual(const.SLOT2TIME[1], '00:00')
        self.assertEqual(const.SLOT2TIME[96], '23:45')
        self.assertEqual(const.SLOT2TIME[10], '02:15')

        with self.assertRaises(KeyError):
            const.SLOT2TIME[0]

        with self.assertRaises(KeyError):
            const.SLOT2TIME[97]

    def test_time2slot(self):
        self.assertEqual(const.TIME2SLOT['00:00'], 1)
        self.assertEqual(const.TIME2SLOT['00:15'], 2)
        self.assertEqual(const.TIME2SLOT['23:45'], 96)
        self.assertEqual(const.TIME2SLOT['23:30'], 95)

        with self.assertRaises(KeyError):
            const.TIME2SLOT['0:00']

        with self.assertRaises(KeyError):
            const.TIME2SLOT['24:00']

    def test_minutes2slot_id(self):
        self.assertEqual(utils.minutes2slot_id(0), 1)
        self.assertEqual(utils.minutes2slot_id(10), 1)
        self.assertEqual(utils.minutes2slot_id(15), 2)
        self.assertEqual(utils.minutes2slot_id(1440), 1)
        self.assertEqual(utils.minutes2slot_id(1439), 96)
        self.assertEqual(utils.minutes2slot_id(30), 3)
        self.assertEqual(utils.minutes2slot_id(31), 3)
        self.assertEqual(utils.minutes2slot_id(44), 3)


if __name__ == '__main__':
    unittest.main()
