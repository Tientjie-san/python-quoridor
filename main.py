from quoridor.src.quoridor import Quoridor

if __name__ == "__main__":
    quoridor = Quoridor()
    invalid_pgn = "e2/e8/a5h/c5h/e5h/g5h/h6v/h7h"
    valid_pgn = "e2/e8/a5h/c5h/e5h/g5h/h6v"
    # quoridor = Quoridor.init_from_pgn(valid_pgn)
    # vmove = "e5k"
    # invalid = "j4"
    # print(bool(ALL_QUORIDOR_MOVES_REGEX.fullmatch(vmove)))
    # print(bool(ALL_QUORIDOR_MOVES_REGEX.fullmatch(invalid)))
    # print(quoridor)
    # print(quoridor.player1)
    quoridor = Quoridor.init_from_pgn(valid_pgn)
    print(quoridor.play_terminal())

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
    print(quoridor.get_pgn())
    # # print(quoridor._wall_out_of_bounds("c8v"))
    # graph = graph = {
    #     "a5": ["a3", "a7"],
    #     "a3": ["a2", "a4"],
    #     "a7": ["a9"],
    #     "a2": [],
    #     "a4": ["a8"],
    #     "a8": [],
    # }
    # print(quoridor._dfs(set(), graph, "a4", "9"))
