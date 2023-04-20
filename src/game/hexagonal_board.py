from typing import List
import numpy as np



class HexagonalBoard:
    "Base class for a hexagonal board"

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.board = self._create_board()

    def _create_board(self) -> List[List["Piece"]]:
        return [[Piece(x, y, None) for x in range(self.x)] for y in range(self.y)]
    
    def change_board(self, state):
        for i, row in enumerate(self.board):
            for j, piece in enumerate(row):
                if state[i * self.x + j] == 1:
                    piece.set_color("red")
                elif state[i * self.x + j] == 2:
                    piece.set_color("blue")

    def place_piece(self, x: int, y: int, color: str):
        if color == None or self.board[y][x].color != None:
             raise Exception(f"Not legal, color: {color}, self.color: {self.board[y][x].color}, x: {x}, y:{y}")
        self.board[y][x].set_color(color)

        

    def print_board(self):
        print(self.board)
    
    def get_empty_tiles(self) -> List["Piece"]:
        empty_tiles = []
        for row in self.board:
            for piece in row:
                if piece.color == None:
                    empty_tiles.append(piece)
        return empty_tiles

    def get_adjacent_tiles(self, piece: 'Piece'):
        directions: List[tuple[int]] = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, 1), (1, -1)]

        # Define a list to store the adjacent tiles
        adjacent_tiles: List[tuple[int]] = []

        # Iterate over each direction
        for dy, dx in directions:
            # Calculate the coordinates of the adjacent tile in this direction
            ny, nx = piece.y + dy, piece.x + dx

            # Check if the adjacent tile is within the bounds of the board
            if ny >= 0 and ny < len(self.board) and nx >= 0 and nx < len(self.board[ny]):
                # Add the coordinates of the adjacent tile to the list
                adjacent_tiles.append((ny, nx))

        #Returning coordinates as pieces
        return [self.board[y][x] for y, x in adjacent_tiles]
    
    def get_tile(self, x: int, y: int):
        return self.board[y][x]
    
    def get_row(self, y: int):
        return self.board[y]
    
    def get_col(self, x: int):
        return [sublist[x] for sublist in self.board]
    
    def get_board(self):
        return self.board


class Piece:
    def __init__(self, x: int, y: int, color: str):
        self.color = color
        self.x = x
        self.y = y

    def set_color(self, color: str):
        if color == None or self.color != None:
            raise Exception("Piece is allready taken")
        self.color = color

    def __str__(self) -> str:
        return self.color

    def __repr__(self) -> str:
        return f"Piece(color={self.color})"
