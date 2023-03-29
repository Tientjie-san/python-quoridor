import string
from typing import Dict, List
from collections import deque
from dataclasses import dataclass


ALL_QUORIDOR_MOVES = [
    string.ascii_letters[i] + str(j) for i in range(9) for j in range(1, 10)
] + [
    string.ascii_letters[i] + str(j) + c
    for i in range(8)
    for j in range(1, 9)
    for c in ["h", "v"]
]


class Quoridor:
    def __init__(self) -> None:
        self.board = self._create_board()
        self.placed_walls = []
        self.legal_walls = set(
            [
                string.ascii_letters[i] + str(j) + c
                for i in range(8)
                for j in range(1, 9)
                for c in ["h", "v"]
            ]
        )
        self.is_terminated = False

    @classmethod
    def init_from_pgn(cls, pgn: str):
        quoridor = cls()
        # validate pgn
        # if valid continue generating the board
        moves = pgn.split("/")
        # for move in moves:
        #     board.
        return quoridor

    def __repr__(self) -> str:
        return f"board: {self.board} \nlegal fences: {self.legal_walls}"

    def __str__(self) -> str:
        return f"board: {self.board} \nlegal fences: {self.legal_walls}"

    def _create_board(self) -> Dict[str, List[str]]:
        board: Dict[str, List[str]] = dict()
        for i in range(9):
            for j in range(1, 10):
                connected_cells = []
                if i != 0:
                    connected_cells.append(string.ascii_letters[i - 1] + str(j))
                if i != 8:
                    connected_cells.append(string.ascii_letters[i + 1] + str(j))
                if j != 1:
                    connected_cells.append(string.ascii_letters[i] + str(j - 1))
                if j != 9:
                    connected_cells.append(string.ascii_letters[i] + str(j + 1))

                board[string.ascii_letters[i] + str(j)] = connected_cells

        return board

    def make_move(self, move: str):
        if move not in ALL_QUORIDOR_MOVES:
            print("illegal move")
        elif len(move) == 2:
            self.make_pawn_move(move)
        else:
            self._make_wall_move((move))

    def _make_pawn_move(self, move: str):
        ...

    def _make_wall_move(self, wall: str):
        if wall not in self.legal_walls:
            print("invalid wall")
        elif wall[2] == "h":
            ...

        elif wall[2] == "v":
            ...
        else:
            print("Invalid wall")

    def get_pgn(self):
        ...

    def get_fen(self):
        ...


if __name__ == "__main__":
    quoridor = Quoridor.init_from_pgn("e2")
    print(quoridor)
