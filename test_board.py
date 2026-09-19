import unittest

from board import Board
from exception import AlreadyShotError, OutOfBoardError
from ship import Ship


class BoardReceiveShotTests(unittest.TestCase):
    def test_out_of_board_coordinates_raise_exception(self):
        board = Board()

        with self.assertRaises(OutOfBoardError):
            board.receive_shot(11, 5)

        with self.assertRaises(OutOfBoardError):
            board.receive_shot(-1, 5)

    def test_repeated_shot_raises_exception(self):
        board = Board()

        self.assertEqual(board.receive_shot(2, 2), "MISS")

        with self.assertRaises(AlreadyShotError):
            board.receive_shot(2, 2)

    def test_hit_is_recorded_and_ship_can_sink(self):
        board = Board()
        board.place_ship(Ship(1), 2, 2, "H")

        self.assertEqual(board.receive_shot(2, 2), "HIT")
        self.assertEqual(board.grid[2][2], 3)
        self.assertTrue(board.check_lose())


if __name__ == "__main__":
    unittest.main()