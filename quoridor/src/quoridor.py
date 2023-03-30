import string
import re
from copy import deepcopy
from typing import Dict, List, Set
from dataclasses import dataclass, field
from exceptions import (
    InvalidMoveError,
    IllegalPawnMoveError,
    IllegalWallPlacementError,
    NoWallToPlaceError,
)


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
        return f"board: {self.board}"

    def __str__(self) -> str:
        return f"board: {self.board}"

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

    def validate_move(self, move: str):
        if not bool(ALL_QUORIDOR_MOVES_REGEX.fullmatch(move)):
            raise InvalidMoveError()
        elif len(move) == 2:
            self._validate_pawn_move(move)
        else:
            self._validate_wall_move(move)

    def make_move(self, move: str):

        self.validate_move(move)
        if len(move) == 2:
            self._make_pawn_move(move)
        else:
            self._make_wall_move((move))
        self._switch_player()

    def get_pgn(self):
        ...

    def get_fen(self):
        ...

    def _switch_player(self) -> None:
        waiting = self.current_player
        self.current_player = self.waiting_player
        self.waiting_player = waiting

    def _validate_pawn_move(self, move):
        if move not in self._legal_pawn_moves():
            raise IllegalPawnMoveError()

    def _validate_wall_move(self, move):
        if self.current_player.walls == 0:
            raise NoWallToPlaceError()
        elif self._wall_out_of_bounds(move):
            raise IllegalWallPlacementError(
                message="Illegal wall placement, wall out of bounds"
            )
        elif self._wall_overlaps(move):
            raise IllegalWallPlacementError(
                message="Illegal wall placements, wall overlaps with another wall"
            )
        # elif not self._is_reachable(self.current_player.pos, self.current_player.goal):
        #     raise IllegalWallPlacementError(
        #         message="Illegal wall placement, you cannot reach your goal"
        #     )
        # elif not self._is_reachable(self.waiting_player.pos, self.waiting_player.goal):
        #     raise IllegalWallPlacementError(
        #         message="Illegal wall placement, opponent cannot reach goal"
        #     )

    def _make_pawn_move(self, move: str):
        self.current_player.pos = move

    def _legal_pawn_moves(self) -> Set[str]:

        """Returns legal pawn moves for the current player"""

        # make a temporary copy of the list
        legal_pawn_moves = self.board[self.current_player.pos][:]

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
                print(pos_behind)
                legal_pawn_moves.append(pos_behind)
            else:
                print(pos_behind)
                print(self.board[self.waiting_player.pos])
                legal_pawn_moves.extend(
                    pos
                    for pos in self.board[self.waiting_player.pos]
                    if pos != self.current_player.pos
                )

        return set(legal_pawn_moves)

    def _wall_overlaps(self, wall: str) -> bool:
        overlapping_walls = []
        if wall[2] == "h":
            overlapping_walls.append(chr(ord(wall[0]) - 1) + wall[1:])
            overlapping_walls.append(chr(ord(wall[0]) + 1) + wall[1:])
            overlapping_walls.append(wall[:2] + "v")
        elif wall[2] == "v":
            overlapping_walls.append(wall[0] + chr(ord(wall[1]) - 1) + wall[2])
            overlapping_walls.append(wall[0] + chr(ord(wall[1]) + 1) + wall[2])
            overlapping_walls.append(wall[:2] + "h")

        for overlapping_wall in overlapping_walls:
            if overlapping_wall in self.placed_walls:
                return True
        return False

    def _wall_out_of_bounds(self, wall) -> bool:
        return wall[0] < "a" or wall[0] > "h" or wall[1] < "1" or wall[1] > "8"

    def _is_reachable(self, player_pos, goal) -> bool:
        ...

    def _make_wall_move(self, wall: str):
        self.placed_walls.append(wall)
        self.current_player.placed_walls.append(wall)
        self.current_player.walls -= 1

        # remove connections
        cell = wall[:2]
        if wall[2] == "h":
            # e3h verwijderd verbinding tussen e3-e4 en f3-f4
            connected_cells = [
                (cell, cell[0] + chr(ord(cell[1]) + 1)),
                (
                    chr(ord(cell[0]) + 1) + cell[1],
                    chr(ord(cell[0]) + 1) + chr(ord(cell[1]) + 1),
                ),
            ]

        else:
            # g6v verwijderd verbinding tussen g6-h6 en g7-h7
            connected_cells = [
                (cell, chr(ord(cell[0]) + 1) + cell[1]),
                (
                    cell[0] + chr(ord(cell[1]) + 1),
                    chr(ord(cell[0]) + 1) + chr(ord(cell[1]) + 1),
                ),
            ]
        for cell_pair in connected_cells:
            # remove cell connections
            if cell_pair[0] in self.board[cell_pair[1]]:
                self.board[cell_pair[1]].remove(cell_pair[0])
            if cell_pair[1] in self.board[cell_pair[0]]:
                self.board[cell_pair[0]].remove(cell_pair[1])


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

    # overlapping_walls = []
    # wall = "g6v"
    # if wall[2] == "h":
    #     # 3 muren kunnen niet meer 1 horizontale muur links, 1 rechts horizontaal, en 1 rechts verticaal
    #     overlapping_walls.append(chr(ord(wall[0]) - 1) + wall[1:])
    #     overlapping_walls.append(chr(ord(wall[0]) + 1) + wall[1:])
    #     overlapping_walls.append(wall[:2] + "v")

    # elif wall[2] == "v":
    #     # 3 muren kunnen niet meer 1 verticale boven, 1 verticale beneden, de laatste 1 boven horizontaal
    #     overlapping_walls.append(wall[0] + chr(ord(wall[1]) - 1) + wall[2])
    #     overlapping_walls.append(wall[0] + chr(ord(wall[1]) + 1) + wall[2])
    #     overlapping_walls.append(wall[:2] + "h")

    # print(overlapping_walls)
    print(quoridor._wall_out_of_bounds("c8v"))
