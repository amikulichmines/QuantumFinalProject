import numpy as np

import sys
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

    def __str__(self):
        if self.id == 0:
            return "oo"
        s = ""
        s += {0: "w", 1: "b"}[self.color]
        s += {1: "p", 2: "n", 3: "k"}[self.id]
        return s

class Chess1D:
    board = []
    completedGames = []
    piecesOnBoard = []
    piecesTaken = []
    possiblePlays = []
    whiteVictoryLogs = []
    blackVictoryLogs = []
    whiteVictoriesByCheckmate = 0
    whiteVictoriesByPieces = 0
    blackVictoriesByCheckmate = 0
    blackVictoriesByPieces = 0
    stalemateLogs = []
    expirationPlays = 5

    def __init__(self, expMoves):
        self.move = {
            0: self.move_space,
            1: self.move_pawn,
            2: self.move_knight,
            3: self.move_king
        }
        self.reset_board()
        self.expirationPlays = int(expMoves * 2)

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
        possiblePlays = []
        for loc in range(len(self.board)):
            if board[loc].color == color and board[loc].id != 0:
                possiblePlays.extend(self.move[board[loc].id](board, loc, board[loc].color, kingSafe=False))
        for possibleBoard in possiblePlays:
            kings = sum([1 for piece in possibleBoard if piece.id == 3])
            if kings < 2:
                return False
        return True

    def stalemate(self, log, board, color):
        piecesLeft = self.pieces_on_board(board)
        if piecesLeft == 2:
            return True, "Only kings left"

        if len(log) >=self.expirationPlays:
            piecesLeft = [self.pieces_on_board(tempboard) for tempboard in log[-self.expirationPlays:]]
            if piecesLeft.count(piecesLeft[0]) == len(piecesLeft):
                return True, "Expiration"

        if not self.calculate_possible_plays(board, color):
            return True, f"Color '{color}' is stuck"

        return False, None

    def pieces_left(self, board, color):
        numPieces = 0
        for piece in board:
            if piece.color == color and piece.id != 0:
                numPieces += 1
        if numPieces == 1:
            return False
        return True

    def pieces_on_board(self, board):
        numPieces = 0
        for piece in board:
            if piece.id != 0:
                numPieces += 1
        return numPieces

    def checkmate(self, board, color):
        if not self.king_is_safe(board, color) and self.calculate_possible_plays(board, color, False) == []:
            a = 3
            return True
        return False

    def move_space(self, board, loc, color):
        return []

    def move_pawn(self, board, loc, color, kingSafe=True, addToPossiblePlays=True):
        nextBoard = board.copy()
        possiblePlays = []
        forward = 1 - 2 * color
        if loc + 1 * forward in range(8):
            target = loc + 1 * forward
            if board[target].color != color or board[loc + 1 * forward].id == 0:
                nextBoard[loc] = Piece(0, 0)
                nextBoard[target] = board[loc]
                if self.king_is_safe(nextBoard, 1 - color) if kingSafe else True:
                    possiblePlays.append(nextBoard)
        return possiblePlays

    def move_knight(self, board, loc, color, kingSafe=True, addToPossiblePlays=True):
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
                    if self.king_is_safe(nextBoard, 1 - color) if kingSafe else True:
                        possiblePlays.append(nextBoard)
        return possiblePlays

    def move_king(self, board, loc, color, kingSafe=True, addToPossiblePlays=True):
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
                    if self.king_is_safe(nextBoard, 1 - color) if kingSafe else True:
                        possiblePlays.append(nextBoard)
        return possiblePlays

    def calculate_possible_plays(self, board, color, append=True):
        possiblePlays = []
        for loc in range(len(self.board)):
            if board[loc].color == color and board[loc].id != 0:
                if append:
                    self.move[board[loc].id](board, loc, board[loc].color)
                possiblePlays.extend(self.move[board[loc].id](board, loc, board[loc].color))
        return possiblePlays

    def get_all_possible_plays(self):
        return [[piece.string_representation() for piece in board] for board in self.possiblePlays]

    def get_best_move_for_white(self):
        self.reset_board()
        possiblePlays = self.calculate_possible_plays(self.board, 0)
        for board in possiblePlays:
            log = [board]
            self.whiteVictoriesByPieces = 0
            self.blackVictoriesByPieces = 0
            self.calculate_all_possible_games(log, board, 1)
            print(f"White wins {self.whiteVictoriesByPieces} times, black wins {self.blackVictoriesByPieces} times.\n"
                  f"White wins {self.whiteVictoriesByPieces / (self.whiteVictoriesByPieces + self.blackVictoriesByPieces+1)} ")
        self.possiblePlays = possiblePlays

    def calculate_all_possible_games(self, log, board, color):
        # initialSize = len(possiblePlays)
        possiblePlays = []
        for loc in range(len(self.board)):
            if board[loc].color == color and board[loc].id != 0:
                possiblePlays.extend(self.move[board[loc].id](board, loc, board[loc].color))

        for newboard in possiblePlays:

            if self.checkmate(newboard, 0):
                self.blackVictoriesByCheckmate += 1
            elif self.checkmate(newboard, 1):
                self.whiteVictoriesByCheckmate += 1
            # if not self.pieces_left(newboard, 1):
            #     self.whiteVictoriesByPieces += 1
            #     self.whiteVictoryLogs.append(log)
            # elif not self.pieces_left(newboard, 0):
            #     self.blackVictoriesByPieces += 1
            #     self.blackVictoryLogs.append(log)
            stalemate, reason = self.stalemate(log, board, color)
            if stalemate:
                # log.append(newboard)
                self.stalemateLogs.append((log, reason))
            else:
                log.append(newboard)
                self.calculate_all_possible_games(log, newboard, 1 - color)


sys.setrecursionlimit(20000)
print(sys.getrecursionlimit())
chess = Chess1D(expMoves=2)
chess.calculate_possible_plays(board=chess.board, color=0)

print("Starting board:\n", [piece.string_representation() for piece in chess.board])
print()
for board in chess.get_all_possible_plays():
    print(board)
print(len(chess.possiblePlays))
chess.get_best_move_for_white()
for log, reason in chess.stalemateLogs:
    print("\nNew Log")
    for board in log:
        print([str(piece) for piece in board])
    print(f"stalemate! {reason}\n")

for log in chess.whiteVictoryLogs:
    print("\nNew Log")
    for board in log:
        print([str(piece) for piece in board])
    print("White victory")

for log in chess.blackVictoryLogs:
    print("\nNew Log")
    for board in log:
        print([str(piece) for piece in board])
    print("Black victory")

print(len(chess.stalemateLogs))
