import numpy as np


class Piece:
    color = ""
    id = 0
    q0 = 0
    q1 = 0
    q2 = 0

    def __init__(self, id, color):
        self.color = color
        self.id = id
        self.q0 = int(bin(id)[2:].zfill(2)[0])
        self.q1 = int(bin(id)[2:].zfill(2)[1])
        self.q2 = int(color)

    def qubit_representation(self):
        return [self.q0, self.q1, self.q2]

    def string_representation(self):
        if self.id == 0:
            return "oo"
        s = ""
        s += {0: "w", 1: "b"}[self.color]
        s += {1: "p", 2: "n", 3: "k"}[self.id]
        return s


class Chess1D:
    pieces = set()
    board = []
    piecesOnBoard = []
    piecesTaken = []
    possiblePlays = []

    def __init__(self):
        self.board = [
            Piece(3, 0),
            Piece(0, 0),
            Piece(2, 1),
            Piece(1, 0),
            Piece(0, 0),
            Piece(1, 1),
            Piece(2, 1),
            Piece(3, 1),
        ]

    def king_is_safe(self, board, color):
        move = {
            0: self.space,
            1: self.pawn,
            2: self.knight,
            3: self.king
        }
        currentboard = [piece.string_representation() for piece in board]
        possiblePlays = []

        for loc in range(len(self.board)):
            if board[loc].color == color and board[loc].id != 0:
                possiblePlays.extend(move[board[loc].id](board, loc, board[loc].color, kingSafe=False))
        newPossiblePlays = [[piece.string_representation() for piece in board] for board in possiblePlays]
        for possibleBoard in possiblePlays:
            kings = sum([1 for piece in possibleBoard if piece.id == 3])
            if kings < 2:
                return False
        return True

    def space(self, board, loc, color):
        pass

    def pawn(self, board, loc, color, kingSafe=True):
        nextBoard = board.copy()
        possiblePlays = []
        forward = 1 - 2 * color
        if loc + 1 * forward in range(8):
            if board[loc + 1 * forward].color != color or board[loc + 1 * forward].id == 0:
                nextBoard[loc] = Piece(0, 0)
                nextBoard[loc + 1 * forward] = board[loc]
                if [piece.qubit_representation() for piece in nextBoard] not in [
                    [piece.qubit_representation() for piece in possible_board] for possible_board in
                    self.possiblePlays] and (self.king_is_safe(nextBoard, 1-color) if kingSafe else True):
                    if kingSafe:
                        self.possiblePlays.append(nextBoard)
                    possiblePlays.append(nextBoard)
        return possiblePlays

    def knight(self, board, loc, color, kingSafe=True):
        forward = 1 - 2 * color
        back = -1 * forward
        possiblePlays = []
        for dir in [forward, back]:
            nextBoard = board.copy()
            target = loc + 2 * dir
            if target in range(8):
                if board[target].color != color or board[target].id == 0:
                    nextBoard[loc] = Piece(0, 0)
                    nextBoard[target] = board[loc]
                    if [piece.qubit_representation() for piece in nextBoard] not in [
                        [piece.qubit_representation() for piece in possible_board] for possible_board in
                        self.possiblePlays] and (self.king_is_safe(nextBoard, 1-color) if kingSafe else True):
                        if kingSafe:
                            self.possiblePlays.append(nextBoard)
                        possiblePlays.append(nextBoard)
        return possiblePlays

    def king(self, board, loc, color, kingSafe=True):
        forward = 1 - 2 * color
        back = -(1 - 2 * color)
        possiblePlays = []
        for dir in [forward, back]:
            nextBoard = board.copy()
            target = loc + 1 * dir
            if target in range(8):
                if board[target].color != color or board[target].id == 0:
                    nextBoard[loc] = Piece(0, 0)
                    nextBoard[target] = board[loc]
                    if [piece.qubit_representation() for piece in nextBoard] not in [
                        [piece.qubit_representation() for piece in possible_board] for possible_board in
                        self.possiblePlays] and (self.king_is_safe(nextBoard, 1-color) if kingSafe else True):
                        if kingSafe:
                            self.possiblePlays.append(nextBoard)
                        possiblePlays.append(nextBoard)
        return possiblePlays

    def get_possible_plays(self, board, color):
        self.possiblePlays = []

        move = {
            0: self.space,
            1: self.pawn,
            2: self.knight,
            3: self.king
        }

        for loc in range(len(self.board)):
            if board[loc].color == color and board[loc].id != 0:
                move[board[loc].id](board, loc, board[loc].color)


        for board in self.possiblePlays:
            print([piece.qubit_representation() for piece in board])

    def calculate_all_possible_games(self, board, color):
        move = {
            0: self.space,
            1: self.pawn,
            2: self.knight,
            3: self.king
        }
        # print("".join([piece.string_representation() for piece in board]))
        initialSize = len(self.possiblePlays)
        for loc in range(len(self.board)):
            if board[loc].color == color and board[loc].id != 0:
                move[board[loc].id](board, loc, board[loc].color)

        for newboard in self.possiblePlays[initialSize:]:
            self.calculate_all_possible_games(newboard, 1 - color)


chess = Chess1D()
chess.get_possible_plays(chess.board, 0)
# chess.calculate_all_possible_games(chess.board, 0)
print([piece.string_representation() for piece in chess.board])
for board in chess.possiblePlays:
    print([piece.string_representation() for piece in board])
print(len(chess.possiblePlays))
