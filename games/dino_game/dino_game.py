import time
import pygame

from games.dino_game import obstacle
from games.dino_game.player import Player
from games.dino_game.obstacle import Obstacle
from games.dino_game.renderer import Renderer
from games.dino_game.score import Score
from games.dino_game.menu import Menu

from difficulty.difficulty_manager import DifficultyManager


class DinoGame:

    WIDTH = 1000
    HEIGHT = 400
    FPS = 60

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT)
        )

        pygame.display.set_caption("Reaction Game")

        self.clock = pygame.time.Clock()

        self.running = True

        self.game_over = False

        self.player = Player()

        self.renderer = Renderer(self.screen)

        self.score = Score()

        self.difficulty = DifficultyManager()

        self.start_time = time.time()

        self.current_time = 0

        self.best_time = 0

        self.level = 1

        self.speed = 6

        self.create_obstacles()

        self.state = "GAME"
        self.menu = Menu()

    def create_obstacles(self):

        if self.level == 1:

            self.speed = 6

            self.obstacles = [
                Obstacle(1000)
            ]

        elif self.level == 2:

            self.speed = 8

            self.obstacles = [
                Obstacle(1000),
                Obstacle(1450)
            ]

        else:

            self.speed = 10

            self.obstacles = [
                Obstacle(1000),
                Obstacle(1450),
                Obstacle(1900)
            ]

    def restart(self):
        self.level = self.difficulty.get_current_game_level()

        self.player.reset()

        self.start_time = time.time()

        self.current_time = 0

        self.game_over = False

        self.score.reset()

        self.menu.reset()

        self.create_obstacles()



    def update(self):
            
            if self.state != "GAME":
                return

            self.current_time = time.time() - self.start_time

            if self.current_time > self.best_time:
                self.best_time = self.current_time

            self.player.update()

            for obstacle in self.obstacles:

                obstacle.update(self.speed)

                if obstacle.get_rect().colliderect(
                    self.player.get_rect()
                ):

                    if not obstacle.hit:

                        print("SCAD 10 PUNCTE")
                        obstacle.hit = True
                        self.difficulty.add_score(-10)
                        print("Scor:", self.difficulty.get_score())
  
                        
                        if self.difficulty.get_score() <= 0:
                            print("GAME OVER")
                            self.game_over = True
                            self.state = "MENU"

                        obstacle.reset()
                        continue

                if (
                    obstacle.get_rect().right
                    < self.player.get_rect().left
                    and not obstacle.passed
                ):

                    obstacle.passed = True

                    self.score.add_points(10)

                    self.difficulty.add_score(10)


    def draw(self):
        if self.state == "GAME":

            self.renderer.draw(

                player=self.player,

                obstacles=self.obstacles,

                score=self.score,

                current_time=self.current_time,

                best_time=self.best_time,

                global_score=self.difficulty.get_score(),

                level=self.level,

                game_over=self.game_over,

                difficulty_messages=self.difficulty.last_change_message
            )
        elif self.state == "MENU":
            self.menu.draw(
                screen=self.screen,
                level=self.level,
                score=self.difficulty.get_score(),
                best_time=self.best_time,
                game_over=self.game_over
            )


    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type != pygame.KEYDOWN:
                continue

            # ESC -> intra/iese din meniu
            if event.key == pygame.K_ESCAPE:

                if self.state == "GAME":
                    self.state = "MENU"
                else:
                    self.state = "GAME"

                continue

            # ================= GAME =================

            if self.state == "GAME":

                if event.key == pygame.K_SPACE:
                    self.player.jump()

            # ================= MENU =================

            else:

                if event.key == pygame.K_UP:
                    self.menu.move_up(
                        self.difficulty.get_score(),
                        self.game_over
                    )

                elif event.key == pygame.K_DOWN:
                    self.menu.move_down(
                        self.difficulty.get_score(),
                        self.game_over
                    )

                elif event.key == pygame.K_RETURN:

                    option = self.menu.get_selected(
                        self.difficulty.get_score(),
                        self.game_over
                    )

                    if option == "Resume":

                        self.state = "GAME"

                    elif option == "Restart":

                        self.restart()
                        self.state = "GAME"

                    elif option == "Increase Difficulty":

                        self.difficulty.increase_game_difficulty()

                        self.restart()

                        self.state = "GAME"

                    elif option == "Decrease Difficulty":

                        self.difficulty.decrease_game_difficulty()

                        self.restart()

                        self.state = "GAME"

                    elif option == "Exit":

                        self.running = False

    def start(self):

        while self.running:

            self.handle_events()

            self.update()

            self.draw()

            self.clock.tick(self.FPS)

        pygame.quit()