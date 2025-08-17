from Balls import *
import random
import math

class Frog(pygame.sprite.Sprite):
    def __init__(self, ball_generator):
        pygame.sprite.Sprite.__init__(self)
        self.balls = ball_generator.images
        self.curr_ball = self.balls[random.randint(0, 5)]
        self.next_ball = self.balls[random.randint(0, 5)]
        self.surface_curr = pygame.image.load(self.curr_ball)
        self.surface_next = pygame.transform.scale(pygame.image.load(self.next_ball), (25,25))

        self.new_size = (110, 110)
        self.original_image = pygame.transform.scale(pygame.image.load("images/Frog.png"), self.new_size)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        (self.rect.x, self.rect.y) = 300, 180

        self.curr_ball_offset = pygame.math.Vector2(0, 40)
        self.next_ball_offset = pygame.math.Vector2(0, -30)
        self.current_angle = 0
        self.curr_ball_pos = None
        self.next_ball_pos = None

    def update(self):
        if self.curr_ball is None:
            self.curr_ball = self.next_ball
            self.next_ball = self.balls[random.randint(0, 5)]
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

        curr_rotated_offset = self.curr_ball_offset.rotate(-self.current_angle)
        next_rotated_offset = self.next_ball_offset.rotate(-self.current_angle)

        self.curr_ball_pos = self.rect.center + curr_rotated_offset
        self.next_ball_pos = self.rect.center + next_rotated_offset

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.curr_ball_pos:
            screen.blit(self.surface_curr, self.surface_curr.get_rect(center=self.curr_ball_pos))
        if self.next_ball_pos:
            screen.blit(self.surface_next, self.surface_next.get_rect(center=self.next_ball_pos))

    def shoot(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        center_x = self.rect.centerx
        center_y = self.rect.centery
        vector_x, vector_y = mouse_x - center_x, mouse_y - center_y

