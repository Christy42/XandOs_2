import pygame

from enum_list import SquareState


class Button:
    def __init__(self, text, rect):
        self.text = text
        self.rect = pygame.Rect(rect)

    def draw(self, screen, font):
        mouse = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse)

        colour = (90, 90, 120) if hovered else (60, 60, 80)

        pygame.draw.rect(screen, colour, self.rect, border_radius=8)
        pygame.draw.rect(screen, (220, 220, 220), self.rect, 2, border_radius=8)

        text = font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


class SquareButton(Button):
    def __init__(self, square, rect):
        super().__init__("", rect)
        self.square = square

    def draw(self, screen, font):
        mouse = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse)

        colour = (90, 90, 120) if hovered else (60, 60, 80)

        pygame.draw.rect(screen, colour, self.rect)
        pygame.draw.rect(screen, (220, 220, 220), self.rect, 2)

        text = font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
        if self.square.symbol == SquareState.O:
            self.draw_O(screen, self.rect)
        elif self.square.symbol == SquareState.X:
            self.draw_X(screen, self.rect)

    def draw_X(self, screen, rect):
        pygame.draw.line(screen, (255, 0, 0)
                         ,[self.rect.centerx-40, self.rect.centery-40],
                         [self.rect.centerx+40, self.rect.centery+40], 15)
        pygame.draw.line(screen, (255, 0, 0)
                         , [self.rect.centerx + 40, self.rect.centery - 40],
                         [self.rect.centerx - 40, self.rect.centery + 40], 15)

    def draw_O(self, screen, rect):
        pygame.draw.circle(screen, (0, 255, 0),
                           rect.center, 60, 10)