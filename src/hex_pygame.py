import pygame
import math
from time import time
from game.hex import HexGame, HexAction
from mcts import MCTS, Node
import parameters as pm

BOARD_SIZE_X = pm.SIZE
BOARD_SIZE_Y = pm.SIZE
BLEED_X = 20
BLEED_Y = 40



# Main game loop
running = True
def run(game: HexGame):
    # Define the size of each hexagon
    hex_size = 40

    # Initialize Pygame
    pygame.init()

    # Set the size of the screen
    screen_size = (1000, 700)
    screen = pygame.display.set_mode(screen_size)

    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    start_time = time()

    

    hex_game = HexGame()

    def is_point_in_hexagon(point_x, point_y, center_x, center_y, size):
        vertices = calculate_hex_vertices(center_x, center_y, size)
        polygon = pygame.draw.polygon(screen, (0, 0, 0, 0), vertices)
        return polygon.collidepoint(point_x, point_y)

    # Define a function to calculate the vertices of a hexagon
    def calculate_hex_vertices(center_x, center_y, size):
        vertices = []
        for i in range(6):
            angle_deg = 60 * i
            angle_rad = math.pi / 180 * angle_deg + math.pi / 6
            x = center_x + size * math.cos(angle_rad) + BLEED_X
            y = center_y + size * math.sin(angle_rad) + BLEED_Y
            vertices.append((x, y))
        return vertices

    # Define a function to draw a hexagon
    def draw_hexagon(center_x, center_y, size, color):
        vertices = calculate_hex_vertices(center_x, center_y, size)
        pygame.draw.polygon(screen, color, vertices)

    # Define a function to draw the hexagonal board
    def draw_board(game: HexGame):
        # Define the size of each hexagon in pixels
        hex_width = hex_size * math.sqrt(3) + 30
        hex_height = hex_size * 2 - 16

        # Define the offset between rows
        row_offset = hex_width * 0.75

        # Define the x and y offset for the first hexagon
        start_x = screen_size[0] / 2 - (BOARD_SIZE_X / 2 * row_offset + hex_width / 2)
        start_y = screen_size[1] / 2 - (BOARD_SIZE_Y / 2 * hex_height + hex_height / 2)

        # Draw the hexagons and labels
        font = pygame.font.SysFont('Arial', 20)
        temp_offset = 0
        for y in range(BOARD_SIZE_Y):
            for x in range(BOARD_SIZE_X):
                center_x = start_x + x * row_offset
                center_y = start_y + y * hex_height
                center_x += temp_offset
                piece = game.board.get_tile(x, y)
                color = BLACK
                if piece.color == "red":
                    color = RED
                elif piece.color == "blue":
                    color = BLUE
                draw_hexagon(center_x, center_y, hex_size, color)

                # Draw row number
                if x == 0:
                    row_text = font.render(str(y + 1), True, BLACK)
                    row_text_rect = row_text.get_rect()
                    row_text_rect.center = (center_x - hex_width / 2 - 20, center_y + 40)
                    screen.blit(row_text, row_text_rect)

                # Draw column letter
                if y == 0:
                    col_text = font.render(chr(x + 65), True, BLACK)
                    col_text_rect = col_text.get_rect()
                    col_text_rect.center = (center_x, center_y - hex_height / 2 - 20)
                    screen.blit(col_text, col_text_rect)
            temp_offset += row_offset / 2
        
    def get_hex_center(row, col):
        hex_width = hex_size * math.sqrt(3) + 30
        hex_height = hex_size * 2 - 16

        row_offset = hex_width * 0.75

        start_x = screen_size[0] / 2 - (BOARD_SIZE_X / 2 * row_offset + hex_width / 2)
        start_y = screen_size[1] / 2 - (BOARD_SIZE_Y / 2 * hex_height + hex_height / 2)

        center_x = start_x + col * row_offset
        center_y = start_y + row * hex_height
        center_x += row_offset / 2 * row
        
        return center_x, center_y

    while time() - start_time < pm.TIME_SHOW:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            """elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for y in range(BOARD_SIZE_Y):
                    for x in range(BOARD_SIZE_X):
                        center_x, center_y = get_hex_center(x, y)
                        if is_point_in_hexagon(mouse_x, mouse_y, center_x, center_y, hex_size):
                            hex_game.do_action(HexAction("red" , y, x))
                            ai = MCTS(hex_game, None, 1)
                            action, none = ai.run()
                            hex_game.do_action(action)
                            if hex_game.is_finished():
                                print(hex_game.get_winner())
                                print(hex_game.board)
"""
        # Draw the screen
        screen.fill(WHITE)
        draw_board(game)
        pygame.display.flip()

    # Clean up
    pygame.quit()