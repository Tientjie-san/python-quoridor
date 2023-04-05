# import unittest
# from quoridor.src.quoridor import *
# from quoridor.src.exceptions import *

# """
# What to test: cases for pawn and fence moves moves, is_game_over
# """


# class TestPawnMoves(unittest.TestCase):
#     def setUp(self) -> None:
#         self.game = Quoridor()

#     def test_pawn_in_corner(self):
#         self.game.current_player.pos = 0, 0
#         legal_moves = {(1, 0), (0, 1)}
#         self.assertEqual(legal_moves, self.game.legal_pawn_moves())

#     def test_pawn_on_edge(self):
#         self.game.current_player.pos = 3, 0
#         legal_moves = {(2, 0), (4, 0), (3, 1)}
#         self.assertEqual(legal_moves, self.game.legal_pawn_moves())

#     def test_fence_blocking_pawn_h(self):
#         self.game.add_fence((4, 4, "H"))
#         self.game.current_player.pos = 4, 4
#         legal_moves = {(3, 4), (4, 3), (4, 5)}
#         self.assertEqual(legal_moves, self.game.legal_pawn_moves())

#     def test_fence_blocking_pawn_v(self):
#         self.game.add_fence((4, 4, "V"))
#         self.game.current_player.pos = 4, 4
#         legal_moves = {(3, 4), (4, 3), (5, 4)}
#         self.assertEqual(legal_moves, self.game.legal_pawn_moves())

#     def test_pawn_facing_opponent(self):
#         self.game.current_player.pos = 4, 4
#         self.game.waiting_player.pos = 5, 4
#         legal_moves = {(3, 4), (4, 3), (4, 5), (6, 4)}
#         self.assertEqual(legal_moves, self.game.legal_pawn_moves())

#     def test_pawn_facing_opponent_on_edge(self):
#         self.game.current_player.pos = 5, 1
#         self.game.waiting_player.pos = 5, 0
#         legal_moves = {(4, 1), (6, 1), (5, 2), (4, 0), (6, 0)}
#         self.assertEqual(legal_moves, self.game.legal_pawn_moves())

#     def test_pawn_facing_opponent_with_wall_behind(self):
#         self.game.add_fence((5, 4, "H"))
#         self.game.current_player.pos = 4, 4
#         self.game.waiting_player.pos = 5, 4
#         legal_moves = {(3, 4), (4, 3), (4, 5), (5, 3), (5, 5)}
#         self.assertEqual(legal_moves, self.game.legal_pawn_moves())

#     def test_pawn_facing_opponent_with_wall_behind_and_right(self):
#         self.game.add_fence((5, 4, "H"))
#         self.game.add_fence((5, 4, "V"))
#         self.game.current_player.pos = 4, 4
#         self.game.waiting_player.pos = 5, 4
#         legal_moves = {(3, 4), (4, 3), (5, 3)}
#         self.assertEqual(legal_moves, self.game.legal_pawn_moves())


# class TestFenceMoves(unittest.TestCase):
#     def setUp(self) -> None:
#         self.game = Quoridor()

#     def test_illegal_fence_overlap(self):
#         self.game.add_fence((4, 5, "H"))
#         self.assertRaises(ValueError, self.game.add_fence, fence=(5, 5, "V"))
#         self.assertRaises(ValueError, self.game.add_fence, fence=(4, 4, "H"))
#         self.assertRaises(ValueError, self.game.add_fence, fence=(4, 6, "H"))

#         self.game.add_fence((3, 3, "V"))
#         self.assertRaises(ValueError, self.game.add_fence, fence=(2, 3, "H"))
#         self.assertRaises(ValueError, self.game.add_fence, fence=(2, 3, "V"))
#         self.assertRaises(ValueError, self.game.add_fence, fence=(4, 3, "V"))

#     def test_illegal_fence_unreachable(self):
#         self.game.add_fence((4, 0, "H"))
#         self.game.add_fence((4, 2, "H"))
#         self.game.add_fence((4, 4, "H"))
#         self.game.add_fence((4, 6, "H"))
#         self.game.add_fence((5, 7, "H"))
#         self.assertRaises(ValueError, self.game.add_fence, fence=(5, 7, "V"))


# class TestEndGame(unittest.TestCase):
#     def setUp(self) -> None:
#         self.game = Quoridor()

#     def test_end_game_p1(self):
#         self.game.current_player.pos = 8, 4
#         self.assertTrue(self.game.is_game_over())

#     def test_end_game_p2(self):
#         self.game.switch_players()
#         self.game.current_player.pos = 0, 4
#         self.assertTrue(self.game.is_game_over())


# if __name__ == "__main__":
#     unittest.main()
