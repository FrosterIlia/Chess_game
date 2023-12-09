import pygame
import time

def constrain(value, min, max):
    return max if value > max else (min if value < min else value)

class Box():
    def __init__(self, win, pos, size):
        self.width = size[0]
        self.height = size[1]
        self.bg = (255,255,255)
        self.font = pygame.font.SysFont('arial', self.height - 8)
        self.text_color = (0, 0, 0)
        self.title = ""
        self.text = self.font.render(self.title, True, (0,0,0))
        self.x = pos[0]
        self.y = pos[1]
        self.win = win
        self.enabled = True
        self.clickFlag = False
        self.is_border = True
        self.border_color = (0, 0, 0)
        self.border_width = 1

    def set_width(self, value):
        self.width = value

    def get_width(self):
        return self.width

    def set_height(self, value):
        self.height = value

    def get_height(self):
        return self.height

    def set_bg(self, value):
        self.bg = value

    def get_bg(self):
        return self.bg

    def set_title(self, value):
        self.title = value
        self.text = self.font.render(self.title, True, (0, 0, 0))

    def get_title(self):
        return self.title

    def set_font(self, value):
        self.font = value
        self.text = self.font.render(self.title, True, (0, 0, 0))

    def get_font(self):
        return self.font

    def set_text_color(self, value):
        self.text_color = value

    def get_text_color(self):
        return self.text_color

    def set_x(self, value):
        self.x = value

    def get_x(self):
        return self.x

    def set_y(self, value):
        self.y = value

    def get_y(self):
        return self.y

    def set_enabled(self, value):
        self.enabled = value

    def get_enabled(self):
        return self.enabled

    def set_is_border(self, value):
        self.is_border = value

    def get_is_border(self):
        return self.is_border

    def set_border_color(self, value):
        self.border_color = value

    def get_border_color(self):
        return self.border_color

    def set_border_width(self, value):
        self.border_width = value

    def get_border_width(self):
        return self.border_width


    def onPress(self):
        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]
        if self.enabled:
            if (pygame.mouse.get_pressed(3)[0] and
                    mouse_x > self.x and
                    mouse_x < self.x + self.width and
                    mouse_y > self.y and
                    mouse_y < self.y + self.height):
                return True
            return False

    def onHover(self):
        if self.enabled:
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]
            if (mouse_x >= self.x and mouse_x <= self.x + self.width and
                    mouse_y >= self.y and mouse_y <= self.y + self.height):
                return True
            return False

    def onClick(self):
        if self.enabled:
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]
            if (pygame.mouse.get_pressed(3)[0] and
                    mouse_x > self.x and
                    mouse_x < self.x + self.width and
                    mouse_y > self.y and
                    mouse_y < self.y + self.height):
                self.clickFlag = True

            if not (pygame.mouse.get_pressed(3)[0] and
                    mouse_x > self.x and
                    mouse_x < self.x + self.width and
                    mouse_y > self.y and
                    mouse_y < self.y + self.height):
                if self.clickFlag == True:
                    self.clickFlag = False
                    return True
            return False

class Button(Box):
    def __init__(self, win, pos, size=(120, 25), title="", color=(207, 159, 27), color_active=(62, 39, 214)):
        Box.__init__(self, win, pos, size)
        self.state = False
        self.color_active = color_active
        self.color = color
        self.title = title

    def set_color_active(self, value):
        self.color_active = value

    def get_color_active(self):
        return self.color_active

    def draw(self):
        if self.onPress():
            self.state = True
        else:
            self.state = False
        if not self.state:
            pygame.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(self.win, self.color_active, (self.x, self.y, self.width, self.height))

        if self.is_border:
            pygame.draw.rect(self.win, self.border_color, (self.x, self.y, self.width, self.height), self.border_width)

        self.win.blit(self.text, (self.x + 4, self.y + 2))

    def get_value(self):
        return self.state


class CheckBox(Box):
    def __init__(self, win, pos, size=(15, 15), bg = (0,0,0)):
        Box.__init__(self, win, pos, size)
        self.state = False
        self.bg = bg

    def draw(self):
        if self.state:
            pygame.draw.rect(self.win, self.border_color, (self.x, self.y, self.width, self.height), self.border_width)
            pygame.draw.rect(self.win, self.bg, (self.x + 2, self.y + 2, self.width - 4, self.height - 4))
        else:
            pygame.draw.rect(self.win, self.border_color, (self.x, self.y, self.width, self.height), self.border_width)

        if self.enabled:
            if self.onClick():
                self.state = not self.state

    def get_value(self):
        return self.state

class FillBox(Box):
    def __init__(self, win, pos, size, min, max,
                 bg = (0, 0, 255),
                 cursor_color = (0, 0, 255),
                 cursor_width = 2,
                 mode = 0):
        Box.__init__(self, win, pos, size)
        self.min = min
        self.max = max
        self.widthF = 0
        self.bg = bg
        self.value = self.min
        self.cursor_color = cursor_color
        self.cursor_width = cursor_width
        self.mode = mode  # 0 - float values, 1 - int values

    def set_mode(self, value):
        self.mode = value

    def get_mode(self):
        return self.mode

    def set_min(self, value):
        self.min = value

    def get_min(self):
        return self.min

    def set_max(self, value):
        self.max = value

    def get_max(self):
        return self.max

    def set_cursor_color(self, value):
        self.cursor_color = value

    def get_cursor_color(self):
        return self.cursor_color

    def set_cursor_width(self, value):
        self.cursor_width = value

    def get_cursor_width(self):
        return self.cursor_width

    def draw(self):
        if self.enabled:
            self.change_value()
        self.text = self.font.render(self.title + " " + str(self.value), True, self.text_color)
        pygame.draw.rect(self.win, self.border_color, (self.x, self.y, self.width, self.height), self.border_width)
        if self.value < self.max:
            pygame.draw.rect(self.win, self.bg, (self.x, self.y, self.widthF, self.height))
        else:
            pygame.draw.rect(self.win, self.bg, (self.x, self.y, self.width, self.height))
        self.win.blit(self.text, (self.x + 4, self.y + 2))

    def change_value(self):
        if self.enabled:
            if self.onPress():
                self.widthF = pygame.mouse.get_pos()[0] - self.x
                if self.widthF > self.width:
                    self.widthF = self.width
                elif self.widthF < 0:
                    self.widthF = 0
                if self.mode == 0:
                    self.value = (self.widthF / self.width) * (self.max - self.min) + self.min
                    self.value = constrain(self.value, self.min, self.max)
                    self.value = round(self.value, 3)
                elif self.mode == 1:
                    self.value = int((self.widthF / self.width) * (self.max - self.min) + self.min)
                    self.value = constrain(self.value, self.min, self.max)


    def get_value(self):
        return self.value



class TextBox(Box):
    def __init__(self, win, pos, size = (120, 25)):
        Box.__init__(self, win, pos, size)
        self.value = ""
        self.visible_text = ""
        self.chosen = False
        self.text_render = self.font.render(self.visible_text, True, self.text_color)
        self.cursor = pygame.Rect(self.x, self.y, 0, self.height)
        self.cursor_pos = 0


    def event_handler(self, event):
        if self.chosen:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.value = self.value[:self.cursor_pos-1] + self.value[self.cursor_pos:]
                    self.cursor_pos -= 1
                elif event.key == pygame.K_LEFT:
                    self.cursor_pos -= 1
                elif event.key == pygame.K_RIGHT:
                    self.cursor_pos += 1

                else:
                    self.value = self.value[:self.cursor_pos] + event.unicode + self.value[self.cursor_pos:]
                    self.cursor_pos += 1

                self.visible_text = ""
                counter = len(self.value) - 1
                while self.font.size(self.visible_text)[0] < self.width - 13 and counter != -1:
                    self.visible_text += self.value[counter]
                    counter -= 1

                self.visible_text = self.visible_text[::-1] # reverse a string
                self.text_render = self.font.render(self.visible_text, True, self.text_color)

                self.cursor_pos = constrain(self.cursor_pos, 0, len(self.visible_text))
    def draw(self):
        pygame.draw.rect(self.win, self.bg, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(self.win, self.border_color, (self.x, self.y, self.width, self.height), self.border_width if not self.chosen else self.border_width + 1)
        self.win.blit(self.text_render, (self.x + 4, self.y + 2))
        if time.time() % 1 > 0.5 and self.chosen:
            self.cursor.width = self.font.size(self.visible_text[0:(len(self.visible_text) - (len(self.value) - self.cursor_pos))])[0]
            pygame.draw.rect(self.win, (0,0,0), (self.cursor.width + self.x + 3, self.y, 2, self.height))

        if pygame.mouse.get_pressed(3)[0] and not self.onPress():
            self.chosen = False
        if self.onClick():
            self.chosen = True
    def get_value(self):
        return self.value

    def clear(self):
        self.value = ""
        self.visible_text = ""
        self.text_render = self.font.render(self.visible_text, True, self.text_color)

    def is_chosen(self):
        return True if self.chosen else False

class Label(Box):
    def __init__(self, win, pos, size = (0,35), text = "hello"):
        Box.__init__(self, win, pos, size)
        self.set_text(text)

    def draw(self):
        self.text = self.font.render(self.title, True, self.text_color)
        self.win.blit(self.text, (self.x, self.y))

    def set_text(self, value):
        self.title = value
        self.text = self.font.render(self.title, True, (0, 0, 0))

    def get_text(self):
        return self.title

    def set_text_height(self, value):
        self.height = value

    def get_text_height(self):
        return self.height

