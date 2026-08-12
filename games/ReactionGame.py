import random
import time


class ReactionGame:

    def __init__(self):

        self.state = None  # "waiting", "ready", "finished"
        self.start_time = None
        self.ready_time = None
        self.reaction_time = None
        self.score = 0

        self.game_over = False


    def start(self):

        # Inițializez un joc nou
        self.state = "waiting"
        self.start_time = time.time()
        self.ready_time = None
        self.reaction_time = None
        self.game_over = False

        # Calculez o întârziere aleatorie (1-3 secunde)
        self.delay = random.uniform(1, 3)

        return self.get_state()


    def check_ready(self):

        # Verificam dacă trebuie să schimbăm starea în "ready"
        if self.state == "waiting":

            elapsed = time.time() - self.start_time

            if elapsed >= self.delay:

                self.state = "ready"
                self.ready_time = time.time()

        return self.get_state()


    def react(self):

        # Utilizatorul a apăsat pe pătrat
        if self.state == "ready":

            # Calculez timpul de reacție
            self.reaction_time = (
                time.time() - self.ready_time
            ) * 1000  # Convertesc în milisecunde

            self.game_over = True
            self.state = "finished"

            # Calculez scorul
            if self.reaction_time < 200:
                self.score = 100

            elif self.reaction_time < 300:
                self.score = 90

            elif self.reaction_time < 400:
                self.score = 80

            elif self.reaction_time < 500:
                self.score = 70

            else:
                self.score = max(
                    50,
                    100 - int(self.reaction_time / 10)
                )

        return self.get_state()


    def get_state(self):

        return {
            "state": self.state,
            "reaction_time": (
                round(self.reaction_time, 2)
                if self.reaction_time
                else None
            ),
            "score": self.score,
            "game_over": self.game_over
        }
