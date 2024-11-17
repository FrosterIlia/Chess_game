import pygame
from copy import deepcopy
from utilities import *
from gui import *

pygame.init()



win = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

pygame.display.set_caption("Chess")

Bp = pygame.image.load("Assets//Bp.png")
Wp = pygame.image.load("Assets//Wp.png")
Bb = pygame.image.load("Assets//Bb.png")
Wb = pygame.image.load("Assets//Wb.png")
Bn = pygame.image.load("Assets//Bn.png")
Wn = pygame.image.load("Assets//Wn.png")
Br = pygame.image.load("Assets//Br.png")
Wr = pygame.image.load("Assets//Wr.png")
Bq = pygame.image.load("Assets//Bq.png")
Wq = pygame.image.load("Assets//Wq.png")
Bk = pygame.image.load("Assets//Bk.png")
Wk = pygame.image.load("Assets//Wk.png")

piece_pictures = {"p": [Bp, Wp],
                  "b": [Bb, Wb],
                  "n": [Bn, Wn],
                  "r": [Br, Wr],
                  "q": [Bq, Wq],
                  "k": [Bk, Wk],
                  }

class Promotion_menu():
    def __init__(self, color):
        self.color = color
        self.width = WIDTH // 4
        self.height = HEIGHT // 4
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT // 2 - self.height // 2
        self.border = 5
        self.cell_width = self.width // 2 - self.border
        self.cell_height = self.height // 2 - self.border
        self.visible = False

        self.buttons_init(color)

    def buttons_init(self, color):
        self.color = color
        self.queen_button = Promotion_button(win,
                                             (self.border + self.x, self.border + self.y),
                                             piece_pictures["q"][color],
                                             "q",
                                             size=(self.cell_width, self.cell_height))
        self.knight_button = Promotion_button(win,
                                              (self.border + self.x + self.cell_width, self.border + self.y),
                                              piece_pictures["n"][color],
                                              "n",
                                              size=(self.cell_width, self.cell_height))
        self.rook_button = Promotion_button(win,
                                            (self.border + self.x, self.border + self.y + self.cell_height),
                                            piece_pictures["r"][color],
                                            "r",
                                            size=(self.cell_width, self.cell_height))
        self.bishop_button = Promotion_button(win,
                                              (self.border + self.x + self.cell_width,
                                               self.border + self.y + self.cell_height),
                                              piece_pictures["b"][color],
                                              "b",
                                              size=(self.cell_width, self.cell_height))

        self.buttons = [self.queen_button, self.knight_button, self.rook_button, self.bishop_button]

    def draw(self):
        if self.visible:
            pygame.draw.rect(win, (255, 255, 255), (self.x, self.y, self.width, self.height))
            for i in self.buttons:
                i.draw()
                i.enabled = True
                if i.onClick():
                    board[promotion_coords[0]][promotion_coords[1]].piece = i.value
                    board[promotion_coords[0]][promotion_coords[1]].piece_color = self.color
                    self.visible = False
                    game.enabled = True

        else:
            for i in self.buttons:
                i.enabled = False

class Promotion_button(Box):
    def __init__(self, win, pos, image, value, size=(120, 25)):

        Box.__init__(self, win, pos, size)
        self.value = value
        self.image = image


    def draw(self):
        win.blit(self.image, (self.x, self.y))


class Game():
    def __init__(self):
        self.white_castle = [1, 1]  # left digit - long castle, right digit - short castle
        self.black_castle = [1, 1]  # left digit - long castle, right digit - short castle
        self.turn = True  # True - white, False - black
        self.enabled = True

    def switch_turn(self):
        self.turn = not self.turn

    def get_turn(self):
        return self.turn

    def get_castle_options(self, color):
        return self.white_castle if color else self.black_castle

    def forbid_castling(self, value, color): # value: 0 - long castle, 1 - short castle, 2 - both
        if color:
            if value == 2:
                self.white_castle = [0,0]
            else:
                self.white_castle[value] = 0

        else:
            if value == 2:
                self.black_castle = [0,0]
            else:
                self.black_castle[value] = 0

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def get_enabled(self):
        return self.enabled


class Cell():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.piece_color = 0
        self.piece = ""  # b - bishop, n - knight, p - pawn, k - king, q - queen, r - rook
        self.clickFlag = False
        self.tag_color = (0, 0, 0)
        self.possible_moves = []
        self.possible_kills = []
        self.possible_castle = []

    def draw(self):
        if self.tag_color == (0, 0, 0):

            pygame.draw.rect(win,
                             BLACK_CELL_COLOR if self.color == 0 else WHITE_CELL_COLOR,
                             (self.x * (CELL_WIDTH + BORDER),
                              self.y * (CELL_HEIGHT + BORDER),
                              CELL_WIDTH,
                              CELL_HEIGHT))
        else:
            pygame.draw.rect(win,
                             self.tag_color,
                             (self.x * (CELL_WIDTH + BORDER),
                              self.y * (CELL_HEIGHT + BORDER),
                              CELL_WIDTH,
                              CELL_HEIGHT))

        if self.piece:
            image = piece_pictures[self.piece][0] if self.piece_color == 0 else piece_pictures[self.piece][1]
            win.blit(image, (self.x * (CELL_WIDTH + BORDER), self.y * (CELL_HEIGHT + BORDER)))

    def set_piece(self, piece, piece_color):
        self.piece = piece
        self.piece_color = piece_color

    def set_tag_color(self, color):
        if color == (0, 0, 120):
            self.tag_color = POSSIBLE_MOVE_COLOR_WHITE if self.color else POSSIBLE_MOVE_COLOR_BLACK
        elif color == (120, 0, 0):
            self.tag_color = POSSIBLE_KILL_COLOR_BLACK
        else:
            self.tag_color = color

    def reset_tag_color(self):
        self.tag_color = (0, 0, 0)

    def on_click(self):
        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]
        if (pygame.mouse.get_pressed(3)[0] and
                mouse_x > self.x * (CELL_WIDTH + BORDER) and
                mouse_x < self.x * (CELL_WIDTH + BORDER) + CELL_WIDTH and
                mouse_y > self.y * (CELL_HEIGHT + BORDER) and
                mouse_y < self.y * (CELL_HEIGHT + BORDER) + CELL_HEIGHT):
            self.clickFlag = True

        if not (pygame.mouse.get_pressed(3)[0] and
                mouse_x > self.x * (CELL_WIDTH + BORDER) and
                mouse_x < self.x * (CELL_WIDTH + BORDER) + CELL_WIDTH and
                mouse_y > self.y * (CELL_HEIGHT + BORDER) and
                mouse_y < self.y * (CELL_HEIGHT + BORDER) + CELL_HEIGHT):
            if self.clickFlag == True:
                self.clickFlag = False
                return True

    def calc_possible_moves(self, board):
        if self.piece:
            if self.piece == "p":
                self.pawn_exec(board)
            elif self.piece == "n":
                self.knight_exec(board)
            elif self.piece == "b":
                self.bishop_exec(board)
            elif self.piece == "r":
                self.rook_exec(board)
            elif self.piece == "q":
                self.queen_exec(board)
            elif self.piece == "k":
                self.king_exec(board)
                if get_king_pos(board, self.piece_color) == [get_chosen().x, get_chosen().y]: # castling
                    self.possible_castle = self.castle_to_coords(self.check_castling())

        else:
            self.possible_kills = []
            self.possible_moves = []
            self.possible_castle = []

    def __repr__(self):
        if self.piece:
            return "W" + self.piece if self.piece_color else "B" + self.piece
        else:
            return ""

    def remove_impossible_moves(self, board):
        for i in self.possible_moves + self.possible_kills:

            temp_board = deepcopy(board)
            temp_board[i[0]][i[1]].piece = self.piece
            temp_board[self.x][self.y].piece = ""
            temp_board[i[0]][i[1]].piece_color = self.piece_color

            if is_check(temp_board, self.piece_color):
                if i in self.possible_moves:
                    self.possible_moves.remove(i)
                else:
                    self.possible_kills.remove(i)

    def calc_moves(self, board):
        self.calc_possible_moves(board)
        self.remove_impossible_moves(board)

    def pawn_exec(self, board):
        self.possible_moves = []
        self.possible_kills = []
        if self.piece_color:  # if white
            if self.y > 0:
                # moving forward
                if not board[self.x][self.y - 1].piece:  # check 1 square up
                    self.possible_moves.append([self.x, self.y - 1])
                    if self.y == 6:
                        if not board[self.x][self.y - 2].piece:  # check 2 square up
                            self.possible_moves.append([self.x, self.y - 2])
                # taking left
                if self.x > 0:
                    if board[self.x - 1][self.y - 1].piece and board[self.x - 1][self.y - 1].piece_color == 0:
                        self.possible_kills.append([self.x - 1, self.y - 1])

                # taking right
                if self.x < COLS - 1:
                    if board[self.x + 1][self.y - 1].piece and board[self.x + 1][self.y - 1].piece_color == 0:
                        self.possible_kills.append([self.x + 1, self.y - 1])


        else:  # black pawn
            # moving forward
            if self.y < 7:
                if not board[self.x][self.y + 1].piece:  # check 1 square down
                    self.possible_moves.append([self.x, self.y + 1])
                    if self.y == 1:
                        if not board[self.x][self.y + 2].piece:  # check 2 square down
                            self.possible_moves.append([self.x, self.y + 2])

                # taking left
                if self.x < COLS - 1:
                    if board[self.x + 1][self.y + 1].piece and board[self.x + 1][self.y + 1].piece_color == 1:
                        self.possible_kills.append([self.x + 1, self.y + 1])

                # taking right
                if self.x > 0:
                    if board[self.x - 1][self.y + 1].piece and board[self.x - 1][self.y + 1].piece_color == 1:
                        self.possible_kills.append([self.x - 1, self.y + 1])

    def knight_exec(self, board):
        self.possible_moves = []
        self.possible_kills = []
        # left down corner
        if self.x >= 1 and self.y <= 5:
            if board[self.x - 1][self.y + 2].piece:
                if board[self.x - 1][self.y + 2].piece_color != self.piece_color:
                    self.possible_kills.append([self.x - 1, self.y + 2])

            else:
                self.possible_moves.append([self.x - 1, self.y + 2])
        if self.x >= 2 and self.y <= 6:
            if board[self.x - 2][self.y + 1].piece:
                if board[self.x - 2][self.y + 1].piece_color != self.piece_color:
                    self.possible_kills.append([self.x - 2, self.y + 1])

            else:
                self.possible_moves.append([self.x - 2, self.y + 1])

        # left up corner
        if self.x >= 1 and self.y >= 2:
            if board[self.x - 1][self.y - 2].piece:
                if board[self.x - 1][self.y - 2].piece_color != self.piece_color:
                    self.possible_kills.append([self.x - 1, self.y - 2])

            else:
                self.possible_moves.append([self.x - 1, self.y - 2])

        if self.x >= 2 and self.y >= 1:
            if board[self.x - 2][self.y - 1].piece:
                if board[self.x - 2][self.y - 1].piece_color != self.piece_color:
                    self.possible_kills.append([self.x - 2, self.y - 1])

            else:
                self.possible_moves.append([self.x - 2, self.y - 1])

        # right up corner
        if self.x <= 5 and self.y >= 1:
            if board[self.x + 2][self.y - 1].piece:
                if board[self.x + 2][self.y - 1].piece_color != self.piece_color:
                    self.possible_kills.append([self.x + 2, self.y - 1])

            else:
                self.possible_moves.append([self.x + 2, self.y - 1])

        if self.x <= 6 and self.y >= 2:
            if board[self.x + 1][self.y - 2].piece:
                if board[self.x + 1][self.y - 2].piece_color != self.piece_color:
                    self.possible_kills.append([self.x + 1, self.y - 2])

            else:
                self.possible_moves.append([self.x + 1, self.y - 2])

        # right down corner
        if self.x <= 6 and self.y <= 5:
            if board[self.x + 1][self.y + 2].piece:
                if board[self.x + 1][self.y + 2].piece_color != self.piece_color:
                    self.possible_kills.append([self.x + 1, self.y + 2])

            else:
                self.possible_moves.append([self.x + 1, self.y + 2])

        if self.x <= 5 and self.y <= 6:
            if board[self.x + 2][self.y + 1].piece:
                if board[self.x + 2][self.y + 1].piece_color != self.piece_color:
                    self.possible_kills.append([self.x + 2, self.y + 1])

            else:
                self.possible_moves.append([self.x + 2, self.y + 1])

    def bishop_exec(self, board):
        self.possible_moves = []
        self.possible_kills = []

        x = self.x
        y = self.y

        # left up
        if not (x <= 0 or y <= 0):
            while not board[x - 1][y - 1].piece and x != 0 and y != 0:
                self.possible_moves.append([x - 1, y - 1])
                if x >= 2 and y >= 2:
                    if board[x - 2][y - 2].piece and board[x - 2][y - 2].piece_color != self.piece_color:
                        self.possible_kills.append([x - 2, y - 2])
                x -= 1
                y -= 1

            # kill check if close
            if x >= 1 and y >= 1:
                if board[x - 1][y - 1].piece and board[x - 1][y - 1].piece_color != self.piece_color:
                    self.possible_kills.append([x - 1, y - 1])

        x = self.x
        y = self.y

        # right up
        if not (x >= 7 or y <= 0):
            while not board[x + 1][y - 1].piece and x != 7 and y != 0:
                self.possible_moves.append([x + 1, y - 1])
                if x <= 5 and y >= 2:
                    if board[x + 2][y - 2].piece and board[x + 2][y - 2].piece_color != self.piece_color:
                        self.possible_kills.append([x + 2, y - 2])

                if x >= 6:
                    break
                x += 1
                y -= 1

            # kill check if close
            if x <= 6 and y >= 1:
                if board[x + 1][y - 1].piece and board[x + 1][y - 1].piece_color != self.piece_color:
                    self.possible_kills.append([x + 1, y - 1])

        x = self.x
        y = self.y

        # right down
        if not (x >= 7 or y >= 7):
            while not board[x + 1][y + 1].piece and x != 7 and y != 7:
                self.possible_moves.append([x + 1, y + 1])
                if x <= 5 and y <= 5:
                    if board[x + 2][y + 2].piece and board[x + 2][y + 2].piece_color != self.piece_color:
                        self.possible_kills.append([x + 2, y + 2])

                if x >= 6 or y >= 6:
                    break
                x += 1
                y += 1

            # kill check if close
            if x <= 6 and y <= 6:
                if board[x + 1][y + 1].piece and board[x + 1][y + 1].piece_color != self.piece_color:
                    self.possible_kills.append([x + 1, y + 1])

        x = self.x
        y = self.y

        # left down
        if not (x <= 0 or y >= 7):

            while not board[x - 1][y + 1].piece and x != 0 and y != 7:

                self.possible_moves.append([x - 1, y + 1])
                if x >= 2 and y <= 5:

                    if board[x - 2][y + 2].piece and board[x - 2][y + 2].piece_color != self.piece_color:
                        self.possible_kills.append([x - 2, y + 2])

                if y >= 6:
                    break
                x -= 1
                y += 1

            # kill check if close
            if x >= 1 and y <= 6:
                if board[x - 1][y + 1].piece and board[x - 1][y + 1].piece_color != self.piece_color:
                    self.possible_kills.append([x - 1, y + 1])

    def rook_exec(self, board):

        self.possible_moves = []
        self.possible_kills = []

        x = self.x
        y = self.y

        # up
        if y > 0:
            while not board[x][y - 1].piece and y != 0:
                self.possible_moves.append([x, y - 1])
                if y >= 2:
                    if board[x][y - 2].piece and board[x][y - 2].piece_color != self.piece_color:
                        self.possible_kills.append([x, y - 2])

                y -= 1

            # kill check if close
            if y >= 1:
                if board[x][y - 1].piece and board[x][y - 1].piece_color != self.piece_color:
                    self.possible_kills.append([x, y - 1])

        x = self.x
        y = self.y

        # right
        if x < 7:

            while not board[x + 1][y].piece and x != 7:

                self.possible_moves.append([x + 1, y])
                if x <= 5:
                    if board[x + 2][y].piece and board[x + 2][y].piece_color != self.piece_color:
                        self.possible_kills.append([x + 2, y])

                if x >= 6:
                    break
                x += 1

            # kill check if close
            if x <= 6:
                if board[x + 1][y].piece and board[x + 1][y].piece_color != self.piece_color:
                    self.possible_kills.append([x + 1, y])

        x = self.x
        y = self.y

        # down
        if y < 7:
            while not board[x][y + 1].piece and y != 7:
                self.possible_moves.append([x, y + 1])
                if y <= 5:
                    if board[x][y + 2].piece and board[x][y + 2].piece_color != self.piece_color:
                        self.possible_kills.append([x, y + 2])

                if y >= 6:
                    break
                y += 1

            # kill check if close
            if y <= 6:
                if board[x][y + 1].piece and board[x][y + 1].piece_color != self.piece_color:
                    self.possible_kills.append([x, y + 1])

        x = self.x
        y = self.y

        # left

        if x > 0:

            while not board[x - 1][y].piece and x != 0:

                self.possible_moves.append([x - 1, y])
                if x >= 2:

                    if board[x - 2][y].piece and board[x - 2][y].piece_color != self.piece_color:
                        self.possible_kills.append([x - 2, y])

                x -= 1

            # kill check if close
            if x >= 1:
                if board[x - 1][y].piece and board[x - 1][y].piece_color != self.piece_color:
                    self.possible_kills.append([x - 1, y])

    def queen_exec(self, board):
        self.possible_moves = []
        self.possible_kills = []

        x = self.x
        y = self.y

        # left up
        if not (x <= 0 or y <= 0):
            while not board[x - 1][y - 1].piece and x != 0 and y != 0:
                self.possible_moves.append([x - 1, y - 1])
                if x >= 2 and y >= 2:
                    if board[x - 2][y - 2].piece and board[x - 2][y - 2].piece_color != self.piece_color:
                        self.possible_kills.append([x - 2, y - 2])
                x -= 1
                y -= 1

            # kill check if close
            if x >= 1 and y >= 1:
                if board[x - 1][y - 1].piece and board[x - 1][y - 1].piece_color != self.piece_color:
                    self.possible_kills.append([x - 1, y - 1])

        x = self.x
        y = self.y

        # right up
        if not (x >= 7 or y <= 0):
            while not board[x + 1][y - 1].piece and x != 7 and y != 0:
                self.possible_moves.append([x + 1, y - 1])
                if x <= 5 and y >= 2:
                    if board[x + 2][y - 2].piece and board[x + 2][y - 2].piece_color != self.piece_color:
                        self.possible_kills.append([x + 2, y - 2])

                if x >= 6:
                    break
                x += 1
                y -= 1

            # kill check if close
            if x <= 6 and y >= 1:
                if board[x + 1][y - 1].piece and board[x + 1][y - 1].piece_color != self.piece_color:
                    self.possible_kills.append([x + 1, y - 1])

        x = self.x
        y = self.y

        # right down
        if not (x >= 7 or y >= 7):
            while not board[x + 1][y + 1].piece and x != 7 and y != 7:
                self.possible_moves.append([x + 1, y + 1])
                if x <= 5 and y <= 5:
                    if board[x + 2][y + 2].piece and board[x + 2][y + 2].piece_color != self.piece_color:
                        self.possible_kills.append([x + 2, y + 2])

                if x >= 6 or y >= 6:
                    break
                x += 1
                y += 1

            # kill check if close
            if x <= 6 and y <= 6:
                if board[x + 1][y + 1].piece and board[x + 1][y + 1].piece_color != self.piece_color:
                    self.possible_kills.append([x + 1, y + 1])

        x = self.x
        y = self.y

        # left down
        if not (x <= 0 or y >= 7):

            while not board[x - 1][y + 1].piece and x != 0 and y != 7:

                self.possible_moves.append([x - 1, y + 1])
                if x >= 2 and y <= 5:

                    if board[x - 2][y + 2].piece and board[x - 2][y + 2].piece_color != self.piece_color:
                        self.possible_kills.append([x - 2, y + 2])

                if y >= 6:
                    break
                x -= 1
                y += 1

            # kill check if close
            if x >= 1 and y <= 6:
                if board[x - 1][y + 1].piece and board[x - 1][y + 1].piece_color != self.piece_color:
                    self.possible_kills.append([x - 1, y + 1])

        x = self.x
        y = self.y

        # up
        if y > 0:
            while not board[x][y - 1].piece and y != 0:
                self.possible_moves.append([x, y - 1])
                if y >= 2:
                    if board[x][y - 2].piece and board[x][y - 2].piece_color != self.piece_color:
                        self.possible_kills.append([x, y - 2])

                y -= 1

            # kill check if close
            if y >= 1:
                if board[x][y - 1].piece and board[x][y - 1].piece_color != self.piece_color:
                    self.possible_kills.append([x, y - 1])

        x = self.x
        y = self.y

        # right
        if x < 7:

            while not board[x + 1][y].piece and x != 7:

                self.possible_moves.append([x + 1, y])
                if x <= 5:
                    if board[x + 2][y].piece and board[x + 2][y].piece_color != self.piece_color:
                        self.possible_kills.append([x + 2, y])

                if x >= 6:
                    break
                x += 1

            # kill check if close
            if x <= 6:
                if board[x + 1][y].piece and board[x + 1][y].piece_color != self.piece_color:
                    self.possible_kills.append([x + 1, y])

        x = self.x
        y = self.y

        # down
        if y < 7:
            while not board[x][y + 1].piece and y != 7:
                self.possible_moves.append([x, y + 1])
                if y <= 5:
                    if board[x][y + 2].piece and board[x][y + 2].piece_color != self.piece_color:
                        self.possible_kills.append([x, y + 2])

                if y >= 6:
                    break
                y += 1

            # kill check if close
            if y <= 6:
                if board[x][y + 1].piece and board[x][y + 1].piece_color != self.piece_color:
                    self.possible_kills.append([x, y + 1])

        x = self.x
        y = self.y

        # left

        if x > 0:

            while not board[x - 1][y].piece and x != 0:

                self.possible_moves.append([x - 1, y])
                if x >= 2:

                    if board[x - 2][y].piece and board[x - 2][y].piece_color != self.piece_color:
                        self.possible_kills.append([x - 2, y])

                x -= 1

            # kill check if close
            if x >= 1:
                if board[x - 1][y].piece and board[x - 1][y].piece_color != self.piece_color:
                    self.possible_kills.append([x - 1, y])

    def king_exec(self, board):
        self.possible_moves = []
        self.possible_kills = []

        # left
        if self.x > 0:
            if board[self.x - 1][self.y].piece:
                if board[self.x - 1][self.y].piece_color != self.piece_color:
                    self.possible_kills.append([self.x - 1, self.y])
            else:
                self.possible_moves.append([self.x - 1, self.y])

        # up
        if self.y > 0:
            if board[self.x][self.y - 1].piece:
                if board[self.x][self.y - 1].piece_color != self.piece_color:
                    self.possible_kills.append([self.x, self.y - 1])
            else:
                self.possible_moves.append([self.x, self.y - 1])

        # right
        if self.x < 7:
            if board[self.x + 1][self.y].piece:
                if board[self.x + 1][self.y].piece_color != self.piece_color:
                    self.possible_kills.append([self.x + 1, self.y])
            else:
                self.possible_moves.append([self.x + 1, self.y])

        # down
        if self.y < 7:
            if board[self.x][self.y + 1].piece:
                if board[self.x][self.y + 1].piece_color != self.piece_color:
                    self.possible_kills.append([self.x, self.y + 1])
            else:
                self.possible_moves.append([self.x, self.y + 1])

        # left up
        if self.x > 0 and self.y > 0:
            if board[self.x - 1][self.y - 1].piece:
                if board[self.x - 1][self.y - 1].piece_color != self.piece_color:
                    self.possible_kills.append([self.x - 1, self.y - 1])
            else:
                self.possible_moves.append([self.x - 1, self.y - 1])

        # right up
        if self.x < 7 and self.y > 0:
            if board[self.x + 1][self.y - 1].piece:
                if board[self.x + 1][self.y - 1].piece_color != self.piece_color:
                    self.possible_kills.append([self.x + 1, self.y - 1])
            else:
                self.possible_moves.append([self.x + 1, self.y - 1])

        # right down
        if self.x < 7 and self.y < 7:
            if board[self.x + 1][self.y + 1].piece:
                if board[self.x + 1][self.y + 1].piece_color != self.piece_color:
                    self.possible_kills.append([self.x + 1, self.y + 1])
            else:
                self.possible_moves.append([self.x + 1, self.y + 1])

        # left down
        if self.x > 0 and self.y < 7:
            if board[self.x - 1][self.y + 1].piece:
                if board[self.x - 1][self.y + 1].piece_color != self.piece_color:
                    self.possible_kills.append([self.x - 1, self.y + 1])
            else:
                self.possible_moves.append([self.x - 1, self.y + 1])


    def move(self, x, y):
        if [x, y] in self.possible_moves or [x, y] in self.possible_kills or [x, y] in self.possible_castle:
            # if king or rook moves, forbid castling
            if self.piece == "k":
                game.forbid_castling(2, self.piece_color)

            if self.piece == "r":
                if self.x == 0:
                    game.forbid_castling(0, self.piece_color)

                if self.x == 7:
                    game.forbid_castling(1, self.piece_color)

            board[x][y].piece = self.piece
            board[x][y].piece_color = self.piece_color
            self.piece = ""


        # this moves rooks in castle
        if [x, y] in self.possible_castle:
            if [x, y] == [2, 7]:
                board[0][7].piece = ""
                board[3][7].piece = "r"
                board[3][7].piece_color = 1

            if [x, y] == [6, 7]:
                board[7][7].piece = ""
                board[5][7].piece = "r"
                board[5][7].piece_color = 1

            if [x, y] == [6, 0]:
                board[7][0].piece = ""
                board[5][0].piece = "r"
                board[5][0].piece_color = 0

            if [x, y] == [2, 0]:
                board[0][0].piece = ""
                board[3][0].piece = "r"
                board[3][0].piece_color = 0

    def check_castling(self):
        castle_results = [False, False]  # [white_long, white_short]

        self.castle = game.get_castle_options(color=self.piece_color)

        # white
        if self.piece == "k":
            if self.piece_color and not is_check(board, 1):
                if self.castle[0]:  # long castle
                    if self.x == 4 and self.y == 7 and board[0][7].piece == "r" and \
                            not board[1][7].piece and not is_threatened(board, not self.piece_color, [1, 7]) and \
                            not board[2][7].piece and not is_threatened(board, not self.piece_color, [2, 7]) and \
                            not board[3][7].piece and not is_threatened(board, not self.piece_color, [3, 7]):
                        castle_results[0] = True

                if self.castle[1]:  # short castle
                    if self.x == 4 and self.y == 7 and board[7][7].piece == "r" and \
                            not board[5][7].piece and not is_threatened(board, not self.piece_color, [5, 7]) and \
                            not board[6][7].piece and not is_threatened(board, not self.piece_color, [6, 7]):
                        castle_results[1] = True

            # black
            if self.piece_color == 0:

                if self.castle[0] and not is_check(board, 0):  # long castle
                    if self.x == 4 and self.y == 0 and board[0][0].piece == "r" and \
                            not board[1][0].piece and not is_threatened(board, not self.piece_color, [1, 0]) and \
                            not board[2][0].piece and not is_threatened(board, not self.piece_color, [2, 0]) and \
                            not board[3][0].piece and not is_threatened(board, not self.piece_color, [3, 0]):
                        castle_results[0] = True

                if self.castle[1] and not is_check(board, 0):  # short castle
                    if self.x == 4 and self.y == 0 and board[7][0].piece == "r" and \
                            not board[5][0].piece and not is_threatened(board, not self.piece_color, [5, 0]) and \
                            not board[6][0].piece and not is_threatened(board, not self.piece_color, [6, 0]):
                        castle_results[1] = True

        return castle_results

    def castle_to_coords(self, castle):
        coords = []
        if self.piece_color:
            if castle[0]:
                coords.append([2, 7])
            if castle[1]:
                coords.append([6, 7])

        else:
            if castle[0]:
                coords.append([2, 0])
            if castle[1]:
                coords.append([6, 0])

        return coords

    def check_pawn_promotion(self):
        print(self.piece, self.x, self.y)
        if self.piece == "p":
            if self.piece_color and self.y == 0:
                return True

            if not self.piece_color and self.y == 7:
                return True

        return False

    def get_possible_moves(self):
        return self.possible_moves

    def get_possible_kills(self):
        return self.possible_kills


def init_cells():
    global board
    flag = 1
    for i in range(COLS):
        temp_array = []
        for j in range(ROWS):
            temp_array.append(Cell(i, j, 1 if flag else 0))
            flag = not flag
        board.append(temp_array)
        flag = not flag

def untag_all():
    for i in board:
        for j in i:
            j.reset_tag_color()

def get_chosen():
    if isChosen:
        return board[chosen[0]][chosen[1]]

def fill_board():
    global board
    # black
    board[0][0].set_piece("r", 0)
    board[1][0].set_piece("n", 0)
    board[2][0].set_piece("b", 0)
    board[3][0].set_piece("q", 0)
    board[4][0].set_piece("k", 0)
    board[5][0].set_piece("b", 0)
    board[6][0].set_piece("n", 0)
    board[7][0].set_piece("r", 0)
    board[0][1].set_piece("p", 0)
    board[1][1].set_piece("p", 0)
    board[2][1].set_piece("p", 0)
    board[3][1].set_piece("p", 0)
    board[4][1].set_piece("p", 0)
    board[5][1].set_piece("p", 0)
    board[6][1].set_piece("p", 0)
    board[7][1].set_piece("p", 0)
    # white
    board[0][7].set_piece("r", 1)
    board[1][7].set_piece("n", 1)
    board[2][7].set_piece("b", 1)
    board[3][7].set_piece("q", 1)
    board[4][7].set_piece("k", 1)
    board[5][7].set_piece("b", 1)
    board[6][7].set_piece("n", 1)
    board[7][7].set_piece("r", 1)
    board[0][6].set_piece("p", 1)
    board[1][6].set_piece("p", 1)
    board[2][6].set_piece("p", 1)
    board[3][6].set_piece("p", 1)
    board[4][6].set_piece("p", 1)
    board[5][6].set_piece("p", 1)
    board[6][6].set_piece("p", 1)
    board[7][6].set_piece("p", 1)

game = Game()
promotion_menu = Promotion_menu(0)

board = []

isChosen = False
chosen = [0, 0]

promotion_coords = []

#game.disable()
init_cells()
fill_board()

run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if isChosen:
        get_chosen().calc_moves(board)
        for i in get_chosen().possible_moves + get_chosen().possible_castle:
            board[i[0]][i[1]].set_tag_color((0, 0, 120))
        for i in get_chosen().possible_kills:
            board[i[0]][i[1]].set_tag_color((120, 0, 0))

    for i in board:
        for j in i:

            j.draw()
            promotion_menu.draw()

            if j.on_click() and game.enabled:
                if not isChosen:
                    untag_all()
                    # if j.piece and j.piece_color == game.get_turn():
                    if j.piece:
                        isChosen = True
                        chosen = [j.x, j.y]
                        get_chosen().set_tag_color(SELECTED_CELL_COLOR)
                    else:
                        untag_all()
                        isChosen = False

                else:
                    if [j.x, j.y] in get_chosen().possible_moves or [j.x, j.y] in get_chosen().possible_kills or \
                                                                    [j.x,j.y] in get_chosen().possible_castle:
                        get_chosen().move(j.x, j.y)
                        if board[j.x][j.y].check_pawn_promotion():
                            game.disable()
                            promotion_menu.buttons_init(board[j.x][j.y].piece_color)
                            promotion_menu.visible = True
                            promotion_coords = [j.x, j.y]

                        game.switch_turn()
                        # calculate checkmate

                        if calc_checkmate(board, not get_chosen().piece_color):
                            pygame.display.set_caption("Checkmate")
                            print("CheckMate")
                        elif is_check(board, not get_chosen().piece_color):
                            print("Check")
                            pygame.display.set_caption("Check")
                        else:
                            pygame.display.set_caption("Chess")



                        isChosen = False
                        untag_all()
                    else:
                        # if j.piece and j.piece_color == game.get_turn():
                        if j.piece:
                            untag_all()
                            isChosen = True
                            chosen = [j.x, j.y]
                            get_chosen().set_tag_color(SELECTED_CELL_COLOR)
                        else:
                            untag_all()
                            isChosen = False
    pygame.display.flip()
    win.fill(pygame.Color("white"))

pygame.quit()
