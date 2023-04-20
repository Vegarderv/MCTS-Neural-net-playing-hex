from typing import List
import numpy as np
from game.hexagonal_board import HexagonalBoard, Piece
from game.game import Game, Action
import parameters as pm


class HexBoard(HexagonalBoard):
    
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
    
    def get_available_tiles(self) -> List["Piece"]:
        return self.get_empty_tiles()

    def _check_if_won(self) -> tuple[bool, str]:
        """Checking if a game is won or not, and by which color"""

        # Checking for each color
        for color in ("red", "blue"):

            # First checking left to right
            left_tiles = list(filter(lambda x: x.color ==
                              color, self.get_col(0)))

            # For each tile that is touching left wall, check if a road can be created to right wall
            for tile in left_tiles:

                used_tiles = []
                current_tiles = [tile]
                while len(current_tiles) != 0:

                    # If tile is toucing right wall, COLOR has won
                    if (current_tiles[0].x == self.x - 1):
                        return [True, color]

                    # Adding all adjacent tiles not in used_tiles
                    current_tiles.extend(
                        list(filter(lambda x: x not in used_tiles and x.color == color,
                                    self.get_adjacent_tiles(current_tiles[0]))))

                    # Removing the current tile and adding it to used_tiles
                    used_tiles.append(current_tiles[0])
                    current_tiles.pop(0)


            # Then checking from top to bottom
            top_tiles = list(filter(lambda x: x.color ==
                              color, self.get_row(0)))        
            for tile in top_tiles:

                used_tiles = []
                current_tiles = [tile]
                while len(current_tiles) != 0:

                    # If tile is toucing right wall, COLOR has won
                    if (current_tiles[0].y == self.y - 1):
                        return [True, color]

                    # Adding all adjacent tiles not in used_tiles
                    current_tiles.extend(
                        list(filter(lambda x: x not in used_tiles and x.color == color,
                                    self.get_adjacent_tiles(current_tiles[0]))))

                    # Removing the current tile and adding it to used_tiles
                    used_tiles.append(current_tiles[0])
                    current_tiles.pop(0)
        return [False, ""]

    def place_piece(self, x: int, y: int, color: str):
        return super().place_piece(x, y, color)
    
    def get_board(self):
        return super().get_board()
    
    def __repr__(self) -> str:
        board = "__________________________\n"
        indent = ""
        for row in self.board:
            for piece in row:
                if piece.color == None:
                    board += f"| {piece.color}"
                else:
                    board += f"| {piece.color} "
            indent += "   "
            board += "|\n" + indent

        board += "‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾"
        return board
    
    def __str__(self) -> str:
        return self.__repr__()

class HexAction(Action):
    def __init__(self, color: str, x: int, y: int) -> None:
        self.color = color
        self.x = x
        self.y = y
    
    def get_info(self):
        return [self.color, self.x, self.y]
    
    def get_action_no(self):
        return self.y * pm.SIZE + self.x


class HexGame(Game):
    def __init__(self, state = None) -> None:
        super().__init__()
        self.board = HexBoard(pm.SIZE, pm.SIZE)
        self.turn = 0
        if state != None:
            self.board.change_board(state)

    
    def get_actions(self) -> list['Action']:
        available =  self.board.get_available_tiles()
        color = "red" if self.turn % 2 == 0 else "blue"
        return list(map(lambda x: HexAction(color, x.x, x.y), available))

    def get_current_color(self):
        return "red" if self.turn == 0 else "blue"
    
    def do_action(self, action: 'HexAction'):
        self.board.place_piece(action.x, action.y, action.color)
        self.turn += 1
    
    def is_finished(self) -> bool:
        return self.board._check_if_won()[0]
    
    def get_winner(self) -> int:
        if self.board._check_if_won()[0]:
            return int(self.board._check_if_won()[1] == "blue")
    
    def get_action(self, no: int):
        return HexAction("red" if self.turn % 2 == 0 else "blue", no % pm.SIZE, no // pm.SIZE)
    
    def get_state(self) -> List[int]:
        color = self.turn % 2
        board = []
        for row in self.board.board:
            for piece in row:
                if piece.color == None:
                    board.append(0)
                elif piece.color == "red":
                    board.append(1)
                else:
                    board.append(2)

        return [color] + board

    def reset(self):
        return self.__init__()
    
        
