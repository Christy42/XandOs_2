import pygame


from display.button import SquareButton, Button
from universal_names import *

class Board:
    def __init__(self, board_state):
        self.state = board_state
        self.square_buttons = []

    def draw(self, screen):
        self.square_buttons = []
        for square in self.state.squares:
            x = self.state.squares[square].x * 200
            y = self.state.squares[square].y * 200-100
            rect = pygame.Rect(x, y, 200, 200)
            self.square_buttons.append(SquareButton(self.state.squares[square], rect))
        for button in self.square_buttons:
            button.draw(screen, button_title_font)


    def handle_event(self, event):
        pass


class BoardEndGame:
    def __init__(self, board, statement):
        self.board = board
        self.statement = statement
        height, width = 45, 1000
        self.start_y = height // 2
        self.x = (width - BUTTON_WIDTH) // 2
        self.buttons = [Button("Main Menu", (self.x, self.start_y, BUTTON_WIDTH, BUTTON_HEIGHT))]

    def draw(self, screen):
        self.board.square_buttons = []
        for square in self.board.squares:
            x = self.board.squares[square].x * 200
            y = self.board.squares[square].y * 200 - 100
            rect = pygame.Rect(x, y, 200, 200)
            self.board.square_buttons.append(SquareButton(self.board.squares[square], rect))
        for button in self.board.square_buttons:
            button.draw(screen, button_title_font)
        for button in self.buttons:
            button.draw(screen, button_font)
        font = pygame.font.Font(None, 80)
        text = font.render(self.statement, True, "yellow")
        rect = text.get_rect(center=(screen.get_width()/2-100, screen.get_height()/2))
        screen.blit(text, rect)

    def handle_event(self, event):
        if self.buttons[0].clicked(event):
            return "main_menu"
        return None
