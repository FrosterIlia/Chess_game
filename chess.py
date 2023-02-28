import pygame
from copy import deepcopy

pygame.init()

WIDTH, HEIGHT = 512, 512
FPS = 120

ROWS = 8
COLS = 8

BORDER = 0
CELL_WIDTH = WIDTH // COLS
CELL_HEIGHT = HEIGHT // ROWS

BLACK_CELL_COLOR = (166, 96, 35)  # (135, 66, 41)
WHITE_CELL_COLOR = (224, 191, 166)  # (235, 183, 80)
SELECTED_CELL_COLOR = (77, 148, 79)
POSSIBLE_MOVE_COLOR_WHITE = (92, 152, 247)
POSSIBLE_MOVE_COLOR_BLACK = (48, 84, 140)
POSSIBLE_KILL_COLOR_WHITE = (247, 92, 92)  # not used
POSSIBLE_KILL_COLOR_BLACK = (156, 40, 40)

win = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()



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
        else:
            self.possible_kills = []
            self.possible_moves = []

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

            if isCheck(temp_board, self.piece_color):
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
        if [x, y] in self.possible_moves or [x, y] in self.possible_kills:
            board[x][y].piece = self.piece
            board[x][y].piece_color = self.piece_color
            self.piece = ""

    def get_possible_moves(self):
        return self.possible_moves

    def get_possible_kills(self):
        return self.possible_kills


board = []

isChosen = False
chosen = [0, 0]


def get_king_pos(board, king_color):
    for col in board:
        for cell in col:
            if cell.piece == "k" and cell.piece_color == king_color:
                return [cell.x, cell.y]


def isCheck(board, king_color):
    for col in board:
        for cell in col:
            if cell.piece_color != king_color:  # checking pieces that can attack king
                cell.calc_possible_moves(board)
                if get_king_pos(board, king_color) in cell.get_possible_kills():
                    return True
    return False


def untag_all():
    for i in board:
        for j in i:
            j.reset_tag_color()


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


def get_chosen():
    if isChosen:
        return board[chosen[0]][chosen[1]]


init_cells()

'''
board[1][7].set_piece("n", 1)  # white knight
board[6][0].set_piece("n", 0)  # black knight
board[7][6].set_piece("p", 1)  # white pawn
board[4][4].set_piece("r", 0)  # black rook
board[7][1].set_piece("p", 0)  # black pawn
board[4][3].set_piece("b", 1)  # white bishop
board[2][2].set_piece("q", 1)  # white queen
board[5][2].set_piece("k", 0)  # black king
board[0][0].set_piece("k", 1)  # white king
'''

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

fill_board()

run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if isChosen:
        get_chosen().calc_moves(board)
        for i in get_chosen().possible_moves:
            board[i[0]][i[1]].set_tag_color((0, 0, 120))
        for i in get_chosen().possible_kills:
            board[i[0]][i[1]].set_tag_color((120, 0, 0))



    for i in board:
        for j in i:

            j.draw()

            if j.on_click():
                if not isChosen:
                    untag_all()
                    if j.piece:
                        isChosen = True
                        chosen = [j.x, j.y]
                        get_chosen().set_tag_color(SELECTED_CELL_COLOR)
                    else:
                        untag_all()
                        isChosen = False

                else:
                    if [j.x, j.y] in get_chosen().possible_moves or [j.x, j.y] in get_chosen().possible_kills:
                        get_chosen().move(j.x, j.y)
                        # calculate checkmate
                        enemy_king_pos = get_king_pos(board,  not get_chosen().piece_color)
                        enemy_king = board[enemy_king_pos[0]][enemy_king_pos[1]]
                        enemy_king.calc_moves(board)
                        if isCheck(board, not get_chosen().piece_color) and\
                                not enemy_king.possible_moves and\
                                not enemy_king.possible_kills:
                            print("Mate")
                        isChosen = False
                        untag_all()
                    else:
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
