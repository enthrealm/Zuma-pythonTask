import pygame
import random
from Constants import *


class Ball(pygame.sprite.Sprite):
    def __init__(self, image_path, pos_in_path, path):
        pygame.sprite.Sprite.__init__(self)

        self.image_path = image_path
        self.pos_in_path = pos_in_path
        self.path = path

        self.image = pygame.image.load(image_path).convert_alpha()
        self.pos = self.path.positions[self.pos_in_path]
        self.rect = self.image.get_rect(center=(round(self.pos.x), round(self.pos.y)))

        self.can_move = True
        self.bonus = None

    def set_position(self, position):
        self.pos_in_path = position
        self.pos = self.path.positions[self.pos_in_path]
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def update(self):
        if self.can_move:
            self.move(1)

    def move(self, steps):
        self.pos_in_path += steps
        if self.pos_in_path >= 0:
            self.pos = pygame.math.Vector2(self.path.positions[self.pos_in_path])
            self.rect.center = (round(self.pos.x), round(self.pos.y))

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def __eq__(self, other):
        return {
                self.image_path == other.image_path and
                self.rect.center == other.rect.center and
                self.can_move == other.can_move
        }


class BallGenerator:
    def __init__(self, path, number):
        self.path = path
        self.number_to_generate = number
        self.number_of_generated = 0
        self.balls = []
        self.images = ["images\Blueball.png", "images\Yellowball.png", "images\Grayball.png",
                       "images\Greenball.png", "images\Purpleball.png", "images\Redball.png"]

    def generate(self):
        if self.number_of_generated < self.number_to_generate:
            if len(self.balls) == 0 or self.balls[0].pos_in_path >= 2 * BALL_RADIUS // self.path.step:
                self.balls.insert(0, Ball(random.choice(self.images), 0, self.path))
                self.number_of_generated += 1

    def move_stopped_ball(self, i):
        if not self.balls[i].can_move:
            if i == 0:
                self.balls[i].can_move = True

            elif self.balls[i - 1].can_move and self.balls[i - 1].rect.colliderect(self.balls[i].rect):
                self.balls[i].can_move = True

    def update_balls(self):
        for i in range(len(self.balls)):
            self.balls[i].update()
            self.move_stopped_ball(i)

    def update_chain(self):
        for i in range(1, len(self.balls)):
            left_ball = self.balls[i - 1]
            right_ball = self.balls[i]
            if right_ball.pos_in_path - left_ball.pos_in_path > 36:
                if left_ball.image_path == right_ball.image_path:
                    self.join_balls(i - 1)
                else:
                    self.stop_balls(i)

    def update(self):
        self.update_chain()
        self.update_balls()

    def draw(self, screen):
        for ball in self.balls:
            ball.draw(screen)

    def get_available_images(self):
        return [ball.image_path for ball in self.balls]

    def insert(self, index, shooting_ball):
        ball = self.convert_shooting_ball(index, shooting_ball)
        self.balls.insert(index + 1, ball)
        for i in range(index + 2, len(self.balls)):
            if self.balls[i].pos_in_path - self.balls[i - 1].pos_in_path >= \
                    2 * BALL_RADIUS // self.path.step:
                break
            self.balls[i].set_position(self.count_next_pos(i - 1))

    def convert_shooting_ball(self, index, shooting_ball):
        ball = Ball(shooting_ball.color,
                    self.count_next_pos(index), self.path)
        ball.can_move = self.balls[index].can_move
        return ball

    def destroy(self, chain):
        for ball in chain:
            self.balls.remove(ball)

    def join_balls(self, index):
        for i in range(index, len(self.balls)):
            self.balls[i].set_position(self.count_next_pos(i - 1))

    def stop_balls(self, tail_index):
        for i in range(tail_index, len(self.balls)):
            self.balls[i].can_move = False

    def count_next_pos(self, index):
        return self.balls[index].pos_in_path + 2 * BALL_RADIUS // self.path.step
