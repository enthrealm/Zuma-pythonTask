import pygame
from Path import Path
from Constants import *
from ui import *
from Balls import *
from Frog import Frog


class Level:
    def __init__(self, number):
        self.number = number
        self.path = Path(number)
        self.ball_generator = BallGenerator(self.path, number * 50)
        self.frog = Frog(self.ball_generator)


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Zuma")

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.level_num = 1
        self.level = Level(self.level_num)
        self.ui_manager = UiManager(self.screen, self.level)
        self.is_quit = False

    def play(self):
        self.continue_game(self.ui_manager.start_game_btn,
                           self.ui_manager.start_game_display)
        while not self.is_quit:
            self.setup_new_game()
            self.play_game()

        pygame.quit()

    def setup_new_game(self):
        self.level = Level(self.level_num)
        self.ui_manager = UiManager(self.screen, self.level)

    def play_game(self):
        game_finished = False

        while not game_finished and not self.is_quit:
            self.level.ball_generator.generate()

            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_quit = True

            self.update_sprites()
            self.update_display(self.ui_manager.game_display)

    def continue_game(self, button, window):
        game_continued = False
        while not game_continued and not self.is_quit:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_quit = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button.rect.collidepoint(mouse):
                        game_continued = True
            self.update_display(window)

    def update_sprites(self):
        self.level.ball_generator.update()
        self.level.frog.update()

    def update_display(self, display):
        self.ui_manager.draw_window(display)
        pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.play()
