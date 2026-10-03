import pygame
from random import randint
import time


from player import Player
from enum_list import *
from display import board_rendering, menu_rendering
from universal_names import *
from board import BoardGame


class BoardState:
    def __init__(self, game):
        self.board = BoardGame()
        self.game = game
        self.renderer = board_rendering.Board(self.board)
        self.turn = 0
        self.winner = None

    def draw(self, screen):
        self.renderer.draw(screen)

    def update(self):
        result = self.board.check_win()

        if result is not None:
            self.winner = result
            return InputState.GAME_OVER

        if self.game.players[self.turn].type == PlayerType.COMPUTER:
            self.computer_turn()
            result = self.board.check_win()
            if result is not None:
                self.winner = result
                return InputState.GAME_OVER

            self.change_turn()

        return InputState.NORMAL

    def handle_input(self, event):
        # if self.game.players[self.turn].type == PlayerType.COMPUTER:
        #     time.sleep(0.1)
        #     self.computer_turn()
        #     self.change_turn()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.renderer.square_buttons:
                if button.clicked(event):
                    b = self.square_clicked(button.square)
                    if b:
                        self.change_turn()

    def change_turn(self):
        self.turn = (self.turn + 1) % 2

    def computer_turn(self):
        move = self.game.players[self.turn].move(self.board)

    def square_clicked(self, square):
        return self.board.make_move(
            (square.x, square.y),
            self.game.players[self.turn].symbol
        )


class EndBoardState:
    def __init__(self, game, board, statement):
        self.board = board
        self.game = game
        self.renderer = board_rendering.BoardEndGame(self.board, statement)
        self.input_state = InputState.NORMAL

    def handle_input(self, event):
        result = self.renderer.handle_event(event)
        if result == "main_menu":
            self.input_state = InputState.MAIN_MENU_PLAYER

    def update(self):
        if self.input_state == InputState.MAIN_MENU_PLAYER:
            return InputState.MAIN_MENU_PLAYER
        return None

    def draw(self, screen):
        self.renderer.draw(screen)



class MainMenuStateChoosePlayers:

    def __init__(self, game):
        self.game = game
        self.input_state = InputState.NORMAL
        self.renderer = menu_rendering.MainMenuPlayer(WIDTH, HEIGHT)

    def handle_input(self, event):
        result = self.renderer.handle_event(event)
        if result in ["computer_vs_computer", "player_vs_player"]:
            if result == "computer_vs_computer":
                self.game.set_player_type([PlayerType.COMPUTER, PlayerType.COMPUTER])
            else:
                self.game.set_player_type([PlayerType.USER, PlayerType.USER])
            self.input_state = InputState.MAIN_MENU_STYLE
        if result == "player_vs_computer":
            self.input_state = InputState.MAIN_MENU_ORDER

    def update(self):
        if self.input_state == InputState.MAIN_MENU_ORDER:
            return InputState.MAIN_MENU_ORDER
        elif self.input_state == InputState.MAIN_MENU_STYLE:
            return InputState.MAIN_MENU_STYLE
        return None

    def draw(self, screen):
        self.renderer.draw(screen)

# 2nd Menu
class MainMenuState:

    def __init__(self, game):
        self.game = game
        self.input_state = InputState.NORMAL
        self.renderer = menu_rendering.MainMenuOrder(WIDTH, HEIGHT)
        self.winner = None

    def handle_input(self, event):
        result = self.renderer.handle_event(event)
        if result in ["random", "player_goes_first", "player_goes_second"]:
            starter = randint(0, 1)
            if (result == "random" and starter == 0) or result == "player_goes_first":
                self.game.set_player_type([PlayerType.USER, PlayerType.COMPUTER])
            else:
                self.game.set_player_type([PlayerType.COMPUTER, PlayerType.USER])
            self.input_state = InputState.MAIN_MENU_STYLE

    def update(self):
        if self.input_state == InputState.MAIN_MENU_STYLE:
            return InputState.MAIN_MENU_STYLE

        return None

    def draw(self, screen):
        self.renderer.draw(screen)

# Last menu
class MainMenuStateChooseSymbol:
    def __init__(self, game):
        self.game = game
        self.input_state = InputState.NORMAL
        self.renderer = menu_rendering.MainMenuStyle(WIDTH, HEIGHT)
        self.winner = None

    def handle_input(self, event):
        result = self.renderer.handle_event(event)
        if result == "X":
            self.game.set_player_symbol(SquareState.X)
            self.input_state = InputState.NEW_GAME
        elif result == "O":
            self.game.set_player_symbol(SquareState.O)
            self.input_state = InputState.NEW_GAME

    def update(self):
        if self.input_state == InputState.NEW_GAME:
            return InputState.NEW_GAME
        return None

    def draw(self, screen):
        self.renderer.draw(screen)


class Game:

    def __init__(self):
        self.starter = 0
        self.state = MainMenuStateChoosePlayers(self)
        self.input_state = InputState.NORMAL
        self.players = [Player(self, PlayerType.COMPUTER, SquareState.X), Player(self, PlayerType.COMPUTER, SquareState.O)]
        self.game_type = None

    def set_game_type(self, game_type):
        self.game_type = game_type

    def set_player_type(self, player_type):
        for i in range(len(self.players)):
            self.players[i].set_player_type(player_type[i])

    def handle_input(self, event):
        self.state.handle_input(event)

    def set_player_symbol(self, player_symbol):
        self.players[0].set_symbol(player_symbol)
        if player_symbol == SquareState.X:
            self.players[1].set_symbol(SquareState.O)
        else:
            self.players[1].set_symbol(SquareState.X)

    def update(self):
        self.input_state = self.state.update()
        if self.input_state == InputState.NEW_GAME:
            self.change_state(BoardState(self))
        elif self.input_state == InputState.MAIN_MENU_PLAYER:
            self.change_state(MainMenuStateChoosePlayers(self))
        elif self.input_state == InputState.MAIN_MENU_ORDER:
            self.change_state(MainMenuState(self))
        elif self.input_state == InputState.MAIN_MENU_STYLE:
            self.change_state(MainMenuStateChooseSymbol(self))
        elif self.input_state == InputState.GAME_OVER:
            if self.players[0].symbol == self.state.winner:
                statement = "Player 1 wins with " + ("X" if self.players[0].symbol == SquareState.X else "O") + "!"
                print("Player 1 wins!")
            elif self.players[1].symbol == self.state.winner:
                statement = "Player 2 wins with " + ("X" if self.players[1].symbol == SquareState.X else "O") + "!"
                print("Player 2 wins!")
            else:
                statement = "Draw!"
                print("Draw!")
            self.state = EndBoardState(self, self.state.board, statement)

    def draw(self, screen):
        self.state.draw(screen)

    def change_state(self, state):
        self.state = state

    def update_player(self, player):
        self.starter = player