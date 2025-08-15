import random
import pygame
import math
from Constants import SCREEN_CENTER
from Balls import *

class Frog(pygame.sprite.Sprite):
    def __init__(self, BallGenerator):
        pygame.sprite.Sprite.__init__(self)
        self.balls = BallGenerator.images
        self.curr_ball = self.balls[random.randint(0,5)]
        self.next_ball = self.balls[random.randint(0,5)]
        self.new_size = (110, 110)
        self.original_image = pygame.transform.scale(pygame.image.load("images/Frog.png"), self.new_size)
        self.image = self.original_image  # Копия для вращения
        self.rect = self.image.get_rect()
        (self.rect.x, self.rect.y) = 300, 180
        self.current_angle = 0

    def update(self):
        if self.curr_ball is None:
            self.curr_ball = self.next_ball
            self.next_ball = self.balls[random.randint(0,5)]
        self.cursor_rotate()

    def cursor_rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        center_x = self.rect.centerx
        center_y = self.rect.centery
        vector_x, vector_y = mouse_x - center_x, mouse_y - center_y

        if math.hypot(vector_x, vector_y) < 5:
            return

        target_angle = math.degrees(-math.atan2(vector_y, vector_x)) + 85

        angle_diff = (target_angle - self.current_angle + 180) % 360 - 180
        self.current_angle += angle_diff * 0.2

        self.image = pygame.transform.rotate(self.original_image, int(self.current_angle))
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

