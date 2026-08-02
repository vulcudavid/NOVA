from games.dino_game.dino_game import DinoGame


class GameManager:

    def __init__(self):

        self.current_game = DinoGame()

    def start(self):

        self.current_game.start()