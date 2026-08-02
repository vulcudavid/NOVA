import pygame


class Renderer:

    def __init__(self, screen):

        self.screen = screen

        self.font = pygame.font.SysFont(
            "Arial",
            24
        )

        self.big_font = pygame.font.SysFont(
            "Arial",
            48,
            bold=True
        )

    def draw(
        self,
        player,
        obstacles,
        score,
        current_time,
        best_time,
        global_score,
        level,
        game_over,
        difficulty_messages=""
    ):

        self.screen.fill((255, 255, 255))

        pygame.draw.line(
            self.screen,
            (0, 0, 0),
            (0, 350),
            (1000, 350),
            3
        )

        pygame.draw.rect(
            self.screen,
            (0, 100, 255),
            player.get_rect()
        )

        for obstacle in obstacles:

            pygame.draw.rect(
                self.screen,
                (220, 50, 50),
                obstacle.get_rect()
            )

        score.draw(self.screen)

        self.screen.blit(
            self.font.render(
                f"Current Time: {current_time:.1f}s",
                True,
                (0, 0, 0)
            ),
            (20, 50)
        )

        self.screen.blit(
            self.font.render(
                f"Best Time: {best_time:.1f}s",
                True,
                (0, 0, 0)
            ),
            (20, 80)
        )

        self.screen.blit(
            self.font.render(
                f"Global Score: {global_score}",
                True,
                (0, 0, 0)
            ),
            (20, 110)
        )

        self.screen.blit(
            self.font.render(
                f"Difficulty: {level}",
                True,
                (0, 0, 0)
            ),
            (20, 140)
        )

        if game_over:

            title = self.big_font.render(
                "GAME OVER",
                True,
                (220, 0, 0)
            )

            self.screen.blit(
                title,
                (320, 80)
            )

            if global_score >= 80:

                msg1 = self.font.render(
                    "Increase difficulty?",
                    True,
                    (0, 0, 255)
                )

                msg2 = self.font.render(
                    "Y = Yes    N = No",
                    True,
                    (0, 0, 0)
                )

                self.screen.blit(msg1, (350, 160))
                self.screen.blit(msg2, (360, 200))

            elif global_score <= 20:

                msg1 = self.font.render(
                    "Decrease difficulty?",
                    True,
                    (0, 0, 255)
                )

                msg2 = self.font.render(
                    "Y = Yes    N = No",
                    True,
                    (0, 0, 0)
                )

                self.screen.blit(msg1, (350, 160))
                self.screen.blit(msg2, (360, 200))

            else:

                restart = self.font.render(
                    "Press SPACE to restart",
                    True,
                    (0, 0, 0)
                )

                self.screen.blit(
                    restart,
                    (340, 180)
                )

            if difficulty_messages != "":

                msg = self.font.render(
                    difficulty_messages,
                    True,
                    (255, 0, 0)
                )

                self.screen.blit(
                    msg,
                    (250, 260)
                )

        pygame.display.flip()