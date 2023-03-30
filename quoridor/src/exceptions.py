class InvalidMoveError(Exception):
    def __init__(self, message="Move is given in an invalid form"):
        self.message = message
        super().__init__(self.message)


class IllegalPawnMoveError(Exception):
    def __init__(self, message="Illegal pawn move."):
        self.message = message
        super().__init__(self.message)


class IllegalWallPlacementError(Exception):
    def __init__(self, message="Illegal wall placement."):
        self.message = message
        super().__init__(self.message)


class NoWallToPlaceError(Exception):
    def __init__(self, message="You have no walls to place"):
        self.message = message
        super().__init__(self.message)
