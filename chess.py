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
    whiteVictoriesByCheckmate = 0
    whiteVictoriesByPieces = 0
    blackVictoriesByCheckmate = 0
    blackVictoriesByPieces = 0

    def __init__(self):
        self.move = {
            0: self.space,
            1: self.pawn,
            2: self.knight,
            3: self.king
        }
        self.reset_board()

    def reset_board(self):
        self.board = [
            Piece(3, 0),
            Piece(2, 0),
            Piece(1, 0),
            Piece(0, 0),
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
        possiblePlays = []
        for loc in range(len(self.board)):
            if board[loc].color == color and board[loc].id != 0:
                possiblePlays.extend(move[board[loc].id](board, loc, board[loc].color, kingSafe=False))
        for possibleBoard in possiblePlays:
            kings = sum([1 for piece in possibleBoard if piece.id == 3])
            if kings < 2:
                return False
        return True

    def pieces_left(self, board, color):
        numPieces = 0
        for piece in board:
            if piece.color == color:
                numPieces += 1
        if numPieces == 1:
            return True
        return False

    def space(self, board, loc, color):
        pass

    def pawn(self, board, loc, color, kingSafe=True, addToPossiblePlays=True):
        nextBoard = board.copy()
        possiblePlays = []
        forward = 1 - 2 * color
        if loc + 1 * forward in range(8):
            target = loc + 1 * forward
            if board[target].color != color or board[loc + 1 * forward].id == 0:
                nextBoard[loc] = Piece(0, 0)
                nextBoard[target] = board[loc]
                if self.king_is_safe(nextBoard, 1-color) if kingSafe else True:
                    self.possiblePlays.append(nextBoard) if kingSafe else None
                    possiblePlays.append(nextBoard)
        return possiblePlays

    def knight(self, board, loc, color, kingSafe=True, addToPossiblePlays=True):
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

    def king(self, board, loc, color, kingSafe=True, addToPossiblePlays=True):
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

    def calculate_possible_plays(self, board, color):
        self.possiblePlays = []

        for loc in range(len(self.board)):
            if board[loc].color == color and board[loc].id != 0:
                self.move[board[loc].id](board, loc, board[loc].color)

    def get_all_possible_plays(self):
        return [[piece.string_representation() for piece in board] for board in self.possiblePlays]

    def get_best_move_for_white(self):
        self.reset_board()
        self.calculate_possible_plays(self.board, 0)
        for board in self.possiblePlays:
            self.whiteVictoriesByPieces = 0
            self.blackVictoriesByPieces = 0
            self.reset_board()
            self.calculate_possible_plays(board, 1)
            for board in self.possiblePlays:
                if not self.pieces_left(board, 1):
                    self.whiteVictoriesByPieces += 1
                if not self.pieces_left(board, 0):
                    self.blackVictoriesByPieces += 1
            print([piece.string_representation() for piece in board])
            print(f"White wins {self.whiteVictoriesByPieces} times, black wins {self.blackVictoriesByPieces} times.\n"
                  f"White wins {self.whiteVictoriesByPieces/(self.whiteVictoriesByPieces+self.blackVictoriesByPieces)} ")

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
chess.calculate_possible_plays(board=chess.board, color=0)

print("Starting board:\n", [piece.string_representation() for piece in chess.board])
print()
chess.get_best_move_for_white()
# for board in chess.get_all_possible_plays():
#     print(board)
# print(len(chess.possiblePlays))
