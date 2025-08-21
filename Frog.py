from Balls import *
from ShootingBall import *
import random
import math
import pygame


class Frog(pygame.sprite.Sprite):
    def __init__(self, ball_generator, bonus_manager, score_manager):
        pygame.sprite.Sprite.__init__(self)
        self.ball_generator = ball_generator
        self.bonus_manager = bonus_manager
        self.score_manager = score_manager
        self.colors = ball_generator.images
        self.curr_ball_color = self.colors[random.randint(0, 5)]
        self.next_ball_color = self.colors[random.randint(0, 5)]
        self.surface_curr = pygame.image.load(self.curr_ball_color)
        self.surface_next = pygame.transform.scale(pygame.image.load(self.next_ball_color), (25, 25))

        self.new_size = (110, 110)
        self.original_image = pygame.transform.scale(pygame.image.load("images/Frog.png"), self.new_size)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 300, 180

        self.curr_ball_offset = pygame.math.Vector2(0, 40)
        self.next_ball_offset = pygame.math.Vector2(0, -30)
        self.current_angle = 0
        self.curr_ball_pos, self.next_ball_pos = None, None

        self.shooting_ball = None

    def update(self):
        if self.curr_ball_color is None:
            self.switch_to_next_ball()
        self.rotate_to_cursor()
        if self.shooting_ball is not None:
            self.shooting_ball.update()

    def switch_to_next_ball(self):
        self.curr_ball_color = self.next_ball_color
        self.surface_curr = pygame.image.load(self.curr_ball_color)
        self.next_ball_color = self.colors[random.randint(0, 5)]
        self.surface_next = pygame.transform.scale(pygame.image.load(self.next_ball_color), (25, 25))

    def rotate_to_cursor(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        frog_x, frog_y = self.rect.centerx, self.rect.centery
        vector_x, vector_y = mouse_x - frog_x, mouse_y - frog_y

        if math.hypot(vector_x, vector_y) < 5:
            return

        target_angle = math.degrees(-math.atan2(vector_y, vector_x)) + 85
        angle_diff = (target_angle - self.current_angle + 180) % 360 - 180
        self.current_angle += angle_diff * 0.2

        self.image = pygame.transform.rotate(self.original_image, int(self.current_angle))
        self.rect = self.image.get_rect(center=self.rect.center)

        curr_rotated_offset = self.curr_ball_offset.rotate(-self.current_angle)
        next_rotated_offset = self.next_ball_offset.rotate(-self.current_angle)

        self.curr_ball_pos = self.rect.center + curr_rotated_offset
        self.next_ball_pos = self.rect.center + next_rotated_offset

    def shoot(self):
        if self.curr_ball_color is None:
            return

        mouse_x, mouse_y = pygame.mouse.get_pos()
        start_x, start_y = self.curr_ball_pos
        vector_x, vector_y = mouse_x - start_x, mouse_y - start_y
        distance = math.hypot(vector_x, vector_y)

        direction = (0, 0)
        if distance > 0:
            direction = (vector_x / distance, vector_y / distance)
        self.shooting_ball = ShootingBall(self.surface_curr, [start_x, start_y], direction,
                                          self.curr_ball_color, self.ball_generator, self.bonus_manager, self.score_manager)

        self.curr_ball_color = None
        self.surface_curr = None

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.surface_curr, self.surface_curr.get_rect(center=self.curr_ball_pos))
        screen.blit(self.surface_next, self.surface_next.get_rect(center=self.next_ball_pos))
        if self.shooting_ball is not None:
            self.shooting_ball.draw(screen)
