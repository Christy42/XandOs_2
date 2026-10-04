import pygame
from random import randint

from player import Player, HumanPlayer, RandomPlayer
from enum_list import *
from display import board_rendering, menu_rendering
from universal_names import *
from board import BoardGame

class State:
    def __init__(self, game):
        self.winner = None
        self.board = None
        self.game = game


class BoardState(State):
    def __init__(self, game):
        super().__init__(game)
        self.board = BoardGame()
        self.renderer = board_rendering.Board(self.board)
        self.turn = game.starter
        self.winner = None

    def draw(self, screen):
        self.renderer.draw(screen)

    def update(self):
        result = self.board.check_win()

        if result is not None:
            self.winner = result
            return InputState.GAME_OVER

        player = self.game.players[self.turn]

        if player.type == PlayerType.COMPUTER:
            self.computer_turn()

            result = self.board.check_win()

            if result is not None:
                self.winner = result
                return InputState.GAME_OVER

            self.change_turn()

        return InputState.NORMAL

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.renderer.square_buttons:
                if button.clicked(event):
                    b = self.square_clicked(button.square)

                    if b:
                        self.change_turn()

    def change_turn(self):
        self.turn = (self.turn + 1) % 2

    def computer_turn(self):
        player = self.game.players[self.turn]

        move = player.choose_move(self.board)
        print("CCC")
        print(move)

        if move is not None:
            return self.board.make_move(
                move,
                player.symbol
            )

        return False

    def square_clicked(self, square):
        player = self.game.players[self.turn]

        return self.board.make_move(
            (square.x, square.y),
            player.symbol
        )


class EndBoardState(State):
    def __init__(self, game, board, statement):
        super().__init__(game)
        self.board = board
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


class MainMenuStateChoosePlayers(State):

    def __init__(self, game):
        super().__init__(game)
        self.input_state = InputState.NORMAL
        self.renderer = menu_rendering.MainMenuPlayer(WIDTH, HEIGHT)

    def handle_input(self, event):
        result = self.renderer.handle_event(event)

        if result == "computer_vs_computer":
            self.game.set_player_type([
                PlayerType.COMPUTER,
                PlayerType.COMPUTER
            ])

            self.input_state = InputState.MAIN_MENU_STYLE

        elif result == "player_vs_player":
            self.game.set_player_type([
                PlayerType.USER,
                PlayerType.USER
            ])

            self.input_state = InputState.MAIN_MENU_STYLE

        elif result == "player_vs_computer":
            self.input_state = InputState.MAIN_MENU_ORDER

    def update(self):
        if self.input_state == InputState.MAIN_MENU_ORDER:
            return InputState.MAIN_MENU_ORDER

        elif self.input_state == InputState.MAIN_MENU_STYLE:
            return InputState.MAIN_MENU_STYLE

        return None

    def draw(self, screen):
        self.renderer.draw(screen)


class MainMenuState(State):

    def __init__(self, game):
        super().__init__(game)
        self.input_state = InputState.NORMAL
        self.renderer = menu_rendering.MainMenuOrder(WIDTH, HEIGHT)

    def handle_input(self, event):
        result = self.renderer.handle_event(event)

        if result == "random":
            self.game.starter = randint(0, 1)

            if self.game.starter == 0:
                self.game.set_player_type([
                    PlayerType.USER,
                    PlayerType.COMPUTER
                ])
            else:
                self.game.set_player_type([
                    PlayerType.COMPUTER,
                    PlayerType.USER
                ])

            self.input_state = InputState.MAIN_MENU_STYLE

        elif result == "player_goes_first":
            self.game.starter = 0

            self.game.set_player_type([
                PlayerType.USER,
                PlayerType.COMPUTER
            ])

            self.input_state = InputState.MAIN_MENU_STYLE

        elif result == "player_goes_second":
            self.game.starter = 1

            self.game.set_player_type([
                PlayerType.COMPUTER,
                PlayerType.USER
            ])

            self.input_state = InputState.MAIN_MENU_STYLE

    def update(self):
        if self.input_state == InputState.MAIN_MENU_STYLE:
            return InputState.MAIN_MENU_STYLE

        return None

    def draw(self, screen):
        self.renderer.draw(screen)


class MainMenuStateChooseSymbol(State):

    def __init__(self, game):
        super().__init__(game)
        self.input_state = InputState.NORMAL
        self.renderer = menu_rendering.MainMenuStyle(WIDTH, HEIGHT)

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

        self.players = [
            Player(SquareState.X),
            Player( SquareState.O)
        ]

        self.game_type = None

    def set_game_type(self, game_type):
        self.game_type = game_type

    def handle_input(self, event):
        self.state.handle_input(event)

    def set_player_type(self, player_types):
        print(player_types)
        self.players = []
        for player_type in player_types:
            if player_type == PlayerType.USER:
                self.players.append(HumanPlayer(SquareState.X))
            elif player_type == PlayerType.COMPUTER:
                self.players.append(RandomPlayer(SquareState.O))

    def set_player_symbol(self, player_symbol):
        self.players[0].symbol = player_symbol

        if player_symbol == SquareState.X:
            self.players[1].symbol = SquareState.O
        else:
            self.players[1].symbol = SquareState.X

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
                statement = (
                    "Player 1 wins with "
                    + ("X" if self.players[0].symbol == SquareState.X else "O")
                    + "!"
                )
                print("Player 1 wins!")

            elif self.players[1].symbol == self.state.winner:
                statement = (
                    "Player 2 wins with "
                    + ("X" if self.players[1].symbol == SquareState.X else "O")
                    + "!"
                )
                print("Player 2 wins!")

            else:
                statement = "Draw!"
                print("Draw!")

            self.state = EndBoardState(
                self,
                self.state.board,
                statement
            )

    def draw(self, screen):
        self.state.draw(screen)

    def change_state(self, state):
        self.state = state

    def update_player(self, player):
        self.starter = player