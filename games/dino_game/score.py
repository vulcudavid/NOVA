import pygame


class Score:

    def __init__(self):

        self.score = 0

        self.font = pygame.font.SysFont(
            "Arial",
            24
        )

    def add_points(self, points):

        self.score += points

    def reset(self):

        self.score = 0

    def get_score(self):

        return self.score

    def draw(self, screen):

        text = self.font.render(
            f"Score: {self.score}",
            True,
            (0, 0, 0)
        )

        screen.blit(
            text,
            (
                20,
                20
            )
        )