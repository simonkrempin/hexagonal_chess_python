import GameBoard
import pygame


class Piece(pygame.sprite.Sprite):

    def __init__(self, starting_tile, screen, white, offset):
        super().__init__()
        self.offset = offset
        self.rect = pygame.Rect(starting_tile.x_pos + self.offset[0], starting_tile.y_pos + self.offset[1], 100, 100)
        self.starting_tile = starting_tile
        self.screen = screen
        self.white = white
        self.current_shows_moves = False
        self.at_start = True

    def show_moves(self):
        print("showing possible moves")

    def delete_moves(self):
        print("don't show moves anymore")

    def move_towards(self, x, y, replace_bottom=True, moved=True):
        self.rect.x = x + self.offset[0]
        self.rect.y = y + self.offset[1]
        if replace_bottom:
            GameBoard.Hexagon(self.starting_tile.screen, self.starting_tile.outer_radius, self.starting_tile.inner_radius, self.starting_tile.x_pos, self.starting_tile.y_pos)
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.display.flip()

        if moved:
            self.at_start = False


def mark_tile(self, tile):
    if not isinstance(tile, GameBoard.Hexagon):
        return None

    if tile.piece is not None:
        if tile.piece.white is self.white:
            return "taken"

        GameBoard.Hexagon(tile.screen, tile.outer_radius, tile.inner_radius, tile.x_pos, tile.y_pos, (255, 0, 0))
        tile.piece.move_towards(tile.x_pos, tile.y_pos, False, False)
        tile.is_destination = True
        return "enemy"

    GameBoard.Hexagon(tile.screen, tile.outer_radius, tile.inner_radius, tile.x_pos, tile.y_pos, (249, 215, 28))
    tile.is_destination = True
    return "field can be destination"


def tile_remove_mark(self, tile):
    if not isinstance(tile, GameBoard.Hexagon):
        return None

    GameBoard.Hexagon(tile.screen, tile.outer_radius, tile.inner_radius, tile.x_pos, tile.y_pos)

    if tile.piece is not None:
        tile.piece.move_towards(tile.x_pos, tile.y_pos, True, False)

    tile.is_destination = False
    return "field no more destination"


class Pawn(Piece):

    def __init__(self, starting_tile, screen, white=False):
        super().__init__(starting_tile, screen, white, (-20, -30))
        if white:
            self.image = pygame.image.load("sprites/white_pawn.png")
        else:
            self.image = pygame.image.load("sprites/black_pawn.png")
        size_x, size_y = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(size_x / 5), int(size_y / 5)))
        screen.blit(self.image, self.rect)

    def show_moves(self):
        if self.white:
            temp_tile = self.starting_tile.top
            if isinstance(temp_tile, GameBoard.Hexagon) and temp_tile.piece is None:
                mark_tile(self, temp_tile)
                temp_tile = temp_tile.top
                if self.at_start and temp_tile is not None and temp_tile != 0 and temp_tile.piece is None:
                    mark_tile(self, temp_tile)
            temp_tile = self.starting_tile.top_right
            if isinstance(temp_tile, GameBoard.Hexagon) and temp_tile.piece is not None:
                mark_tile(self, temp_tile)
            temp_tile = self.starting_tile.top_left
            if isinstance(temp_tile, GameBoard.Hexagon) and temp_tile.piece is not None:
                mark_tile(self, temp_tile)
        else:
            temp_tile = self.starting_tile.bottom
            if temp_tile is not None and temp_tile != 0 and temp_tile.piece is None:
                mark_tile(self, temp_tile)
                temp_tile = temp_tile.bottom
                if self.at_start and temp_tile is not None and temp_tile != 0 and temp_tile.piece is None:
                    mark_tile(self, temp_tile)
            temp_tile = self.starting_tile.bottom_right
            if temp_tile is not None and temp_tile != 0 and temp_tile.piece is not None:
                mark_tile(self, temp_tile)
            temp_tile = self.starting_tile.bottom_left
            if temp_tile is not None and temp_tile != 0 and temp_tile.piece is not None:
                mark_tile(self, temp_tile)
        self.current_shows_moves = True

    def delete_moves(self):
        if self.white:
            temp_tile = self.starting_tile.top
            if temp_tile is not None and temp_tile != 0 and temp_tile.piece is None:
                tile_remove_mark(self, temp_tile)
                temp_tile = temp_tile.top
                if self.at_start and temp_tile is not None and temp_tile != 0 and temp_tile.piece is None:
                    tile_remove_mark(self, temp_tile)
            temp_tile = self.starting_tile.top_right
            if temp_tile is not None and temp_tile != 0 and temp_tile.piece is not None:
                tile_remove_mark(self, temp_tile)
            temp_tile = self.starting_tile.top_left
            if temp_tile is not None and temp_tile != 0 and temp_tile.piece is not None:
                tile_remove_mark(self, temp_tile)
        else:
            temp_tile = self.starting_tile.bottom
            if temp_tile is not None and temp_tile != 0 and temp_tile.piece is None:
                tile_remove_mark(self, temp_tile)
                temp_tile = temp_tile.bottom
                if self.at_start and temp_tile is not None and temp_tile != 0 and temp_tile.piece is None:
                    tile_remove_mark(self, temp_tile)
            temp_tile = self.starting_tile.bottom_right
            if temp_tile is not None and temp_tile != 0 and temp_tile.piece is not None:
                tile_remove_mark(self, temp_tile)
            temp_tile = self.starting_tile.bottom_left
            if temp_tile is not None and temp_tile != 0 and temp_tile.piece is not None:
                tile_remove_mark(self, temp_tile)
        self.current_shows_moves = False


class King(Piece):

    def __init__(self, starting_tile, screen, white=False):
        super().__init__(starting_tile, screen, white, (-30, -30))
        if white:
            self.image = pygame.image.load("sprites/white_king.png")
        else:
            self.image = pygame.image.load("sprites/black_king.png")
        size_x, size_y = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(size_x / 5), int(size_y / 5)))
        screen.blit(self.image, self.rect)

    def show_moves(self):
        i = 0
        for tile in self.starting_tile.sides:
            temp_value = 1+i if 1+i < 6 else 0
            mark_tile(self, tile.sides[temp_value]) if mark_tile(self, tile) is not None else False
            i += 1

    def delete_moves(self):
        i = 0
        for tile in self.starting_tile.sides:
            temp_value = 1 + i if 1 + i < 6 else 0
            tile_remove_mark(self, tile.sides[temp_value]) if tile_remove_mark(self, tile) is not None else False
            i += 1


class Rook(Piece):

    def __init__(self, starting_tile, screen, white=False):
        super(Rook, self).__init__(starting_tile, screen, white, (-30, -30))
        self.sprite = None
        self.rows = []

        if white:
            self.image = pygame.image.load("sprites/white_rook.png")
        else:
            self.image = pygame.image.load("sprites/black_rooks.png")
        size_x, size_y = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(size_x / 5), int(size_y / 5)))
        screen.blit(self.image, self.rect)

    def show_moves(self):
        self.rows = [[], [], [], [], [], []]
        for i in range(len(self.starting_tile.sides)):
            tile = self.starting_tile.sides[i]
            while mark_tile(self, tile) is not None:
                self.rows[i].append(tile)
                if tile.piece is not None:
                    break
                tile = tile.sides[i]

    def delete_moves(self):
        self.current_shows_moves = False
        for row in self.rows:
            for tile in row:
                tile_remove_mark(self, tile)


class Bishop(Piece):

    def __init__(self, starting_tile, screen, white=False):
        super(Bishop, self).__init__(starting_tile, screen, white, (-27, -35))
        self.sprite = None
        self.rows = []

        if white:
            self.image = pygame.image.load("sprites/white_bishop.png")
        else:
            self.image = pygame.image.load("sprites/black_bishop.png")
        size_x, size_y = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(size_x / 5.5), int(size_y / 5.5)))
        screen.blit(self.image, self.rect)

    def show_moves(self):
        self.rows = [[], [], [], [], [], []]
        for i in range(len(self.starting_tile.sides)):
            tile = self.starting_tile
            if tile.sides[i] is None or tile.sides[i] == 0:
                continue
            else:
                tile = tile.sides[i].sides[i + 1 if i + 1 < 6 else 0]
            while mark_tile(self, tile) is not None:
                self.rows[i].append(tile)
                if tile.piece is not None:
                    tile = None
                    continue
                if tile.sides[i] is None or tile.sides[i] == 0:
                    tile = None
                else:
                    tile = tile.sides[i].sides[i + 1 if i + 1 < 6 else 0]

    def delete_moves(self):
        self.current_shows_moves = False
        for row in self.rows:
            for tile in row:
                tile_remove_mark(self, tile)


class Queen(Piece):

    def __init__(self, starting_tile, screen, white=False):
        super(Queen, self).__init__(starting_tile, screen, white, (-30, -30))
        self.sprite = None
        self.rows = []

        if white:
            self.image = pygame.image.load("sprites/white_queen.png")
        else:
            self.image = pygame.image.load("sprites/black_queen.png")
        size_x, size_y = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(size_x / 5), int(size_y / 5)))
        screen.blit(self.image, self.rect)

    def show_moves(self):
        self.rows = [[], [], [], [], [], []]
        # copied bishop behaviour movement
        for i in range(len(self.starting_tile.sides)):
            tile = self.starting_tile
            if tile.sides[i] is None or tile.sides[i] == 0:
                continue
            else:
                tile = tile.sides[i].sides[i + 1 if i + 1 < 6 else 0]

            while mark_tile(self, tile) is not None:
                self.rows[i].append(tile)
                if tile.piece is not None:
                    tile = None
                    continue
                if tile.sides[i] is None or tile.sides[i] == 0:
                    tile = None
                else:
                    tile = tile.sides[i].sides[i + 1 if i + 1 < 6 else 0]

        # copied rook behaviour of movement
        for i in range(len(self.starting_tile.sides)):
            tile = self.starting_tile.sides[i]
            while mark_tile(self, tile) is not None:
                self.rows[i].append(tile)
                if tile.piece is not None:
                    break
                tile = tile.sides[i]

    def delete_moves(self):
        self.current_shows_moves = False
        for row in self.rows:
            for tile in row:
                tile_remove_mark(self, tile)


class Knight(Piece):

    def __init__(self, starting_tile, screen, white=False):
        super(Knight, self).__init__(starting_tile, screen, white, (-30, -30))
        self.sprite = None
        self.tiles = []

        if white:
            self.image = pygame.image.load("sprites/white_knight.png")
        else:
            self.image = pygame.image.load("sprites/black_knight.png")
        size_x, size_y = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(size_x / 5), int(size_y / 5)))
        screen.blit(self.image, self.rect)

    def show_moves(self):
        for i in range(len(self.starting_tile.sides)):
            if self.starting_tile.sides[i] is not None and self.starting_tile.sides[i] != 0:
                if self.starting_tile.sides[i].sides[i] is not None and self.starting_tile.sides[i].sides[i] != 0:
                    tile = self.starting_tile.sides[i].sides[i].sides[5+i if 5+i < 6 else 5+i-6]
                    if mark_tile(self, tile) is not None:
                        self.tiles.append(tile)
                    tile = self.starting_tile.sides[i].sides[i].sides[1+i if i+1 < 6 else i+1-6]
                    if mark_tile(self, tile) is not None:
                        self.tiles.append(tile)

    def delete_moves(self):
        self.current_shows_moves = False
        for tile in self.tiles:
            tile_remove_mark(self, tile)
