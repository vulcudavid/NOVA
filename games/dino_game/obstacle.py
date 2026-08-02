import pygame
import random


class Obstacle:

    WIDTH = 40
    HEIGHT = 60

    FLOOR_Y = 290

    def __init__(self, start_x):

        self.start_x = start_x
        self.hit = False

        self.rect = pygame.Rect(
            start_x,
            self.FLOOR_Y,
            self.WIDTH,
            self.HEIGHT
        )

        self.passed = False

    def update(self, speed):

        self.rect.x -= speed

        if self.rect.right < 0:
            self.reset()

    def reset(self):

        self.rect.x = random.randint(1000, 1400)
        self.hit = False

        self.passed = False

    def get_rect(self):
        return self.rect