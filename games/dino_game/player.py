import pygame


class Player:

    WIDTH = 50
    HEIGHT = 50

    START_X = 120
    FLOOR_Y = 300

    GRAVITY = 0.8
    JUMP_FORCE = -16

    def __init__(self):
        self.rect = pygame.Rect(
            self.START_X,
            self.FLOOR_Y,
            self.WIDTH,
            self.HEIGHT
        )

        self.velocity = 0
        self.on_ground = True

    def update(self):

        self.velocity += self.GRAVITY
        self.rect.y += self.velocity

        if self.rect.y >= self.FLOOR_Y:
            self.rect.y = self.FLOOR_Y
            self.velocity = 0
            self.on_ground = True

    def jump(self):

        if self.on_ground:
            self.velocity = self.JUMP_FORCE
            self.on_ground = False

    def reset(self):

        self.rect.x = self.START_X
        self.rect.y = self.FLOOR_Y
        self.velocity = 0
        self.on_ground = True

    def get_rect(self):
        return self.rect