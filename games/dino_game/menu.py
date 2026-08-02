import pygame


class Menu:

    def __init__(self):

        self.font = pygame.font.SysFont("Arial", 32)
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)

        self.selected = 0

    def get_options(self, score, game_over):

        options = []

        if not game_over:
            options.append("Resume")

        options.append("Restart")

        if score >= 80:
            options.append("Increase Difficulty")

        elif score <= 20:
            options.append("Decrease Difficulty")

        options.append("Exit")

        return options

    def move_up(self, score, game_over):

        options = self.get_options(score, game_over)

        self.selected -= 1

        if self.selected < 0:
            self.selected = len(options) - 1

    def move_down(self, score, game_over):

        options = self.get_options(score, game_over)

        self.selected += 1

        if self.selected >= len(options):
            self.selected = 0

    def get_selected(self, score, game_over):

        options = self.get_options(score, game_over)

        return options[self.selected]

    def reset(self):

        self.selected = 0

    def draw(
        self,
        screen,
        level,
        score,
        best_time,
        game_over
    ):

        screen.fill((240, 240, 240))

        if game_over:

            title = self.title_font.render(
                "GAME OVER",
                True,
                (200, 0, 0)
            )

        else:

            title = self.title_font.render(
                "GAME MENU",
                True,
                (0, 0, 0)
            )

        screen.blit(title, (320, 30))

        info = [

            f"Difficulty : {level}",

            f"Global Score : {score}",

            f"Best Time : {best_time:.1f} s"

        ]

        y = 120

        for text in info:

            surface = self.font.render(
                text,
                True,
                (0, 0, 0)
            )

            screen.blit(surface, (70, y))

            y += 40

        y = 260

        options = self.get_options(score, game_over)

        for index, option in enumerate(options):

            color = (0, 120, 255)

            if index == self.selected:
                color = (220, 0, 0)

            text = self.font.render(
                option,
                True,
                color
            )

            screen.blit(text, (330, y))

            y += 50

        help_text = self.font.render(
            "UP/DOWN = Navigate   ENTER = Select",
            True,
            (80, 80, 80)
        )

        screen.blit(help_text, (180, 360))

        pygame.display.flip()