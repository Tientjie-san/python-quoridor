import string
import re
from copy import deepcopy
from typing import Dict, List, Set
from collections import deque
from dataclasses import dataclass, field
from exceptions import InvalidMoveError, IllegalPawnMoveError, IllegalWallPlacementError


ALL_QUORIDOR_MOVES_REGEX = re.compile(r"[a-i][1-9](?:[hv])?")

START_POS_P1 = "e4"
GOAL_P1 = 9
START_POS_P2 = "e3"
GOAL_P2 = 1
START_WALLS = 10


@dataclass
class Player:

    id: int
    pos: str
    goal: int
    walls: int = START_WALLS
    placed_walls: List[str] = field(default_factory=lambda: [])


class Quoridor:
    def __init__(self) -> None:
        self.board = self._create_board()
        self.player1 = Player(id=1, pos=START_POS_P1, goal=GOAL_P1)
        self.player2 = Player(id=2, pos=START_POS_P2, goal=GOAL_P2)
        self.current_player = self.player1
        self.waiting_player = self.player2
        self.placed_walls = []
        self.legal_walls = [
            string.ascii_letters[i] + str(j) + c
            for i in range(8)
            for j in range(1, 9)
            for c in ["h", "v"]
        ]
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
        if not bool(ALL_QUORIDOR_MOVES_REGEX.fullmatch(move)):
            raise InvalidMoveError()
        elif len(move) == 2:
            self._make_pawn_move(move)
        else:
            self._make_wall_move((move))
        self.switch_player()

    def _make_pawn_move(self, move: str):
        if move not in self._legal_pawn_moves():
            raise IllegalPawnMoveError()
        else:
            self.current_player.pos = move

    def _legal_pawn_moves(self) -> Set[str]:

        """Returns legal pawn moves for the current player"""
        legal_pawn_moves = self.board[self.current_player.pos]
        # check if the other player is in range of current player for jumping moves
        if self.waiting_player.pos in legal_pawn_moves:
            legal_pawn_moves.remove(self.waiting_player.pos)
            # same row
            if self.current_player.pos[1] == self.waiting_player.pos[1]:
                if self.current_player.pos[0] > self.waiting_player.pos[0]:
                    pos_behind = (
                        chr(ord(self.current_player.pos[0]) - 2)
                        + self.current_player.pos[1]
                    )
                else:
                    pos_behind = (
                        chr(ord(self.current_player.pos[0]) + 2)
                        + self.current_player.pos[1]
                    )

            elif (
                self.current_player.pos[0] == self.waiting_player.pos[0]
            ):  # same column
                if self.current_player.pos[1] > self.waiting_player.pos[1]:
                    pos_behind = self.current_player.pos[0] + chr(
                        ord(self.current_player.pos[1]) - 2
                    )
                else:
                    pos_behind = self.current_player.pos[0] + chr(
                        ord(self.current_player.pos[1]) + 2
                    )
            if pos_behind in self.board[self.waiting_player.pos]:
                legal_pawn_moves.append(pos_behind)
            else:
                legal_pawn_moves.extend(
                    pos
                    for pos in self.board[self.waiting_player.pos]
                    if pos != self.current_player.pos
                )

        return set(legal_pawn_moves)

    def _wall_overlaps(self, wall) -> bool:
        ...

    def _wall_out_of_bounds(self, wall) -> bool:
        ...

    def _is_reachable(self, player_pos, goal) -> bool:
        ...

    def _make_wall_move(self, wall: str):
        if wall not in self.legal_walls:
            raise IllegalWallPlacementError()
        elif self._wall_out_of_bounds:
            raise IllegalWallPlacementError(
                message="Illegal wall placement, wall out of bounds"
            )
        elif not self._is_reachable(self.current_player.pos, self.current_player.goal):
            raise IllegalWallPlacementError(
                message="Illegal wall placement, cannot reach your goal"
            )
        elif not self._is_reachable(self.waiting_player.pos, self.waiting_player.goal):
            raise IllegalWallPlacementError(
                message="Illegal wall placement, opponent cannot reach goal"
            )
        self.placed_walls.append(wall)
        # remove connections

    def get_pgn(self):
        ...

    def get_fen(self):
        ...

    def switch_player(self) -> None:
        waiting = self.current_player
        self.current_player = self.waiting_player
        self.waiting_player = waiting


if __name__ == "__main__":
    quoridor = Quoridor.init_from_pgn("e2")
    # vmove = "e5k"
    # invalid = "j4"
    # print(bool(ALL_QUORIDOR_MOVES_REGEX.fullmatch(vmove)))
    # print(bool(ALL_QUORIDOR_MOVES_REGEX.fullmatch(invalid)))
    # print(quoridor)
    # print(quoridor.player1)
    command = ""
    while command != "q":
        print(f"current player: {quoridor.current_player}")
        print(f"waiting player: {quoridor.waiting_player}")
        print(f"legal_moves {quoridor._legal_pawn_moves()}")
        command = input("Your move: ")
        if command == "q":
            break
        quoridor.make_move(command)
