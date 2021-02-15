import GameBoard
import pygame
import math
import pieces
import time

pygame.init()
radius = 40
outer_radius = radius
inner_radius = radius * (math.sqrt(3) / 2)
screen = pygame.display.set_mode((math.floor(12 * math.sqrt(math.pow(outer_radius, 2) - math.pow(inner_radius, 2)) + 100 + 10 * outer_radius), math.floor(20 * inner_radius + 100)))
screen.fill((255, 255, 255))
game_board = GameBoard.GameBoard(screen, outer_radius, inner_radius)
hexagons = game_board.return_hexagons()
current_selected_piece = None

whites_turn = True
running = True
while running:
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            x_pos, y_pos = pygame.mouse.get_pos()
            for hexa_array in hexagons:
                find = False
                for hexa in hexa_array:
                    if type(hexa) == int:
                        continue
                    distance_to_hexa_x = abs(x_pos - hexa.x_pos)
                    distance_to_hexa_y = abs(y_pos - hexa.y_pos)
                    if distance_to_hexa_y <= inner_radius and distance_to_hexa_x <= inner_radius:
                        if hexa.is_destination:
                            current_selected_piece.delete_moves()
                            current_selected_piece.move_towards(hexa.x_pos, hexa.y_pos)
                            current_selected_piece.starting_tile.piece = None
                            current_selected_piece.starting_tile = hexa
                            current_selected_piece.move_towards(hexa.x_pos, hexa.y_pos)
                            # if the King gets beaten the other team wins
                            if type(hexa.piece) is pieces.King:
                                pygame.font.init()
                                my_font = pygame.font.SysFont('Comic Sans MS', 30)
                                text_surface = my_font.render('der Sieger ist' + (' weiß' if whites_turn else ' schwarz'), False, (0, 0, 0))
                                screen.blit(text_surface, (0, 0))
                                pygame.display.flip()
                                time.sleep(5)
                                running = False
                                pygame.quit()
                            hexa.piece = current_selected_piece
                            current_selected_piece = None
                            # if pawn reaches the other side of the game board he becomes a queen
                            if type(hexa.piece) is pieces.Pawn and ((hexa.piece.white is True and hexa.changer_level == 1) or (hexa.piece.white is False and hexa.changer_level == 2)):
                                hexa.piece = pieces.Queen(hexa, screen, hexa.piece.white)
                                hexa.piece.move_towards(hexa.x_pos, hexa.y_pos)

                            whites_turn = not whites_turn
                        elif hexa.piece is not None:
                            # who's turn is it
                            if whites_turn == hexa.piece.white:
                                if current_selected_piece is not hexa.piece and current_selected_piece is not None:
                                    current_selected_piece.delete_moves()
                                current_selected_piece = hexa.piece
                                if hexa.piece.current_shows_moves:
                                    hexa.piece.delete_moves()
                                else:
                                    hexa.piece.show_moves()
                                find = True
                                break
                            elif current_selected_piece is not None:
                                current_selected_piece.delete_moves()
                                current_selected_piece = None
                        # if clicked somewhere else then on a turns piece or destination delete all possible moves
                        elif current_selected_piece is not None:
                            current_selected_piece.delete_moves()
                            current_selected_piece = None
                if find:  # skip more iterations through the hexagon array so not two pieces can't be selected
                    break
