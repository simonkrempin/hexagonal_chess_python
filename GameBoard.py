import pygame
import math
# import random
import Pieces


class Hexagon:

    def __init__(self, screen, outer_radius, inner_radius, x, y, color=(205, 133, 63)):
        self.screen = screen
        self.outer_radius = outer_radius
        self.inner_radius = inner_radius
        self.x_pos: float
        self.y_pos: float
        self.rect_obj = None
        self.color = color
        self.piece = None
        self.is_destination = False
        self.changer_level = 0  # 0 if no level up field 1 if white level up side 2 if black level up side

        # neighbors
        self.top = None
        self.top_right = None
        self.bottom_right = None
        self.bottom = None
        self.bottom_left = None
        self.top_left = None
        self.sides = [self.top, self.top_right, self.bottom_right, self.bottom, self.bottom_left, self.top_left]

        # create the hexagon
        self.x_pos = x
        self.y_pos = y
        # positions of the corners where the middle of the hexagon is x and y
        corner_positions = [
            (x + self.outer_radius, y),
            (x + 0.5 * self.outer_radius, y + self.inner_radius),
            (x - 0.5 * self.outer_radius, y + self.inner_radius),
            (x - self.outer_radius, y),
            (x - 0.5 * self.outer_radius, y - self.inner_radius),
            (x + 0.5 * self.outer_radius, y - self.inner_radius)
        ]

        pygame.draw.polygon(self.screen, color, corner_positions)
        self.rect_obj = pygame.draw.polygon(self.screen, (0, 0, 0), corner_positions, width=3)

    def define_neighbor(self, top, top_right, bottom_right, bottom, bottom_left, top_left):
        self.top = top
        self.top_right = top_right
        self.bottom_right = bottom_right
        self.bottom = bottom
        self.bottom_left = bottom_left
        self.top_left = top_left
        self.sides = [self.top, self.top_right, self.bottom_right, self.bottom, self.bottom_left, self.top_left]


class GameBoard:

    def __init__(self, screen, outer_radius, inner_radius):
        half_edge = math.sqrt(math.pow(outer_radius, 2) - math.pow(inner_radius, 2))

        self.fields = []

        # creating the game board
        # upper half of the game board until the only piece with the len of 10
        for y in range(6):
            arr = []
            for x in range(6 + y):
                x_pos = 75 + (x * (half_edge + outer_radius))
                y_pos = 230 + inner_radius * 2 * y - inner_radius * x
                arr.append(Hexagon(screen, outer_radius, inner_radius, x_pos, y_pos))
            self.fields.append(arr)
        # lower half of the game board
        for y in range(5):
            arr = []
            for i in range(y + 1):
                arr.append(0)
            for x in range(10 - y):
                x_pos = y * (outer_radius + half_edge) + 75 + outer_radius + half_edge + (x * (half_edge + outer_radius))
                y_pos = 610 + inner_radius * y - inner_radius * x
                arr.append(Hexagon(screen, outer_radius, inner_radius, x_pos, y_pos))
            self.fields.append(arr)

        # for every piece assign the neighbor pieces -> top, top_right, bottom_right, bottom, bottom_left, top_left
        # None if neighbor piece in that direction is 0 or None
        for i in range(len(self.fields)):
            for j in range(len(self.fields[i])):
                top = None if i == 0 or (len(self.fields[i - 1]) < len(self.fields[i]) == j + 1) else self.fields[i - 1][j]
                top_right = self.fields[i][j + 1] if len(self.fields[i]) > j + 1 else None
                bottom_right = None if i == 10 or (i >= 5 and j >= len(self.fields[i + 1]) - 1) else self.fields[i + 1][j + 1]
                bottom = None if i >= 10 else self.fields[i + 1][j]
                bottom_left = None if j == 0 else self.fields[i][j - 1]
                top_left = None if j == 0 or i == 0 else self.fields[i - 1][j - 1]

                if type(self.fields[i][j]) == int:
                    continue
                self.fields[i][j].define_neighbor(top, top_right, bottom_right, bottom, bottom_left, top_left)

        # setup pieces on board False if black piece white if white piece
        # black pieces
        # bishops
        for i in range(3):
            self.fields[i][5].piece = Pieces.Bishop(self.fields[i][5], screen, False)
        # queen
        self.fields[0][4].piece = Pieces.Queen(self.fields[0][4], screen, False)
        # king
        self.fields[1][6].piece = Pieces.King(self.fields[1][6], screen, False)
        # knights
        self.fields[0][3].piece = Pieces.Knight(self.fields[0][3], screen, False)
        self.fields[2][7].piece = Pieces.Knight(self.fields[2][7], screen, False)
        # rooks
        self.fields[0][2].piece = Pieces.Rook(self.fields[0][2], screen, False)
        self.fields[3][8].piece = Pieces.Rook(self.fields[3][8], screen, False)
        # pawns
        for i in range(5):
            self.fields[0 + i][1 + i].piece = Pieces.Pawn(self.fields[0 + i][1 + i], screen, False)
        for i in range(4):
            self.fields[4][6 + i].piece = Pieces.Pawn(self.fields[4][6 + i], screen, False)

        # white pieces
        # bishops
        for i in range(3):
            self.fields[10-i][5].piece = Pieces.Bishop(self.fields[10-i][5], screen, True)
        # queen
        self.fields[9][4].piece = Pieces.Queen(self.fields[9][4], screen, True)
        # king
        self.fields[10][6].piece = Pieces.King(self.fields[10][6], screen, True)
        # knights
        self.fields[8][3].piece = Pieces.Knight(self.fields[8][3], screen, True)
        self.fields[10][7].piece = Pieces.Knight(self.fields[10][7], screen, True)
        # rooks
        self.fields[7][2].piece = Pieces.Rook(self.fields[7][2], screen, True)
        self.fields[10][8].piece = Pieces.Rook(self.fields[10][8], screen, True)
        # pawns
        for i in range(5):
            self.fields[6][1+i].piece = Pieces.Pawn(self.fields[6][1+i], screen, True)
        for i in range(4):
            self.fields[7+i][6+i].piece = Pieces.Pawn(self.fields[7+i][6+i], screen, True)

        # assign changer value to edge pieces
        # black side of pieces / white level up side
        for i in range(11):
            if i < 6:
                self.fields[0][i].changer_level = 1
            else:
                self.fields[i-5][i].changer_level = 1
        # white side of pieces / black level up side
        for i in range(11):
            if i < 6:
                self.fields[5+i][i].changer_level = 2
            else:
                self.fields[10][i].changer_level = 2

    def return_hexagons(self):
        return self.fields
