from Balls import *


class ShootingBall:
    def __init__(self, surface, start_pos, direction, color, ball_generator):
        self.surface = surface
        self.pos = list(start_pos)
        self.direction = direction
        self.speed = 17
        self.active = True
        self.color = color
        self.ball_generator = ball_generator


    def update(self):
        if not self.active:
            return
        collision_result = self.check_collision(self.ball_generator.balls)
        if collision_result is not None:
            hit_ball, index = collision_result
            self.ball_generator.insert(index, self)
            self.check_for_matches(index + 1)
            self.deactivate()
            return

        self.pos[0] += self.direction[0] * self.speed
        self.pos[1] += self.direction[1] * self.speed

        if self.is_out_of_bounds():
            self.deactivate()

    def check_for_matches(self, inserted_index):
        balls = self.ball_generator.balls

        if not (0 <= inserted_index < len(balls)):
            return

        target_color = balls[inserted_index].image_path

        left = inserted_index
        while left > 0 and balls[left - 1].image_path == target_color:
            left -= 1

        right = inserted_index
        while right < len(balls) - 1 and balls[right + 1].image_path == target_color:
            right += 1

        if right - left + 1 >= 3:
            del balls[left:right + 1]

    def is_out_of_bounds(self):
        return (self.pos[0] < -50 or self.pos[0] > WIDTH + 50 or
                self.pos[1] < -50 or self.pos[1] > HEIGHT + 50)

    def check_collision(self, balls):
        if not self.active:
            return None

        shot_rect = self.surface.get_rect(center=self.pos)

        for index, ball in enumerate(self.ball_generator.balls):
            if shot_rect.colliderect(ball.rect):
                return ball, index
        return None

    def draw(self, screen):
        if self.active:
            screen.blit(self.surface, self.surface.get_rect(center=self.pos))

    def deactivate(self):
        self.active = False