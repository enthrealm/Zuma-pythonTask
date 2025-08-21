import pygame
from Constants import *


class Star(pygame.sprite.Sprite):
    def __init__(self, path, balls, score_manager):
        pygame.sprite.Sprite.__init__(self)

        self.balls = balls
        self.score_manager = score_manager

        self.image = pygame.transform.smoothscale(
            pygame.image.load('images/star.png'), (80, 80))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=path.positions[-1])

    def update(self):
        for ball in self.balls:
            if self.rect.colliderect(ball.rect):
                self.score_manager.lose()

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
