import unittest
import Model


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.model = Model.MinesweeperModel()

    def test_isWin(self):
        self.assertEqual(self.model.isWin(), False)

    def test_isGameOver(self):
        self.assertEqual(self.model.isGameOver(), False)

    def test_nextCellMark(self):
        self.assertEqual(self.model.nextCellMark(10, 10), False)

    def test_time_convert(self):
        self.assertEqual(self.model.time_convert(10), "00:00:10")


if __name__ == '__main__':
    unittest.main()
