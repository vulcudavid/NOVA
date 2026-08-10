import random


class MemoryGame:

    def __init__(self):

        self.cards = []
        self.revealed = []
        self.matched = []

        self.score = 0
        self.attempts = 0
        self.level = 1

        self.game_over = False


    def start(self, level=1):

        self.level = level

        # Numărul de perechi crește odată cu nivelul
        pairs = min(3 + level - 1, 10)

        self.cards = list(range(pairs)) * 2

        random.shuffle(self.cards)

        self.revealed = []
        self.matched = []

        self.score = 0
        self.attempts = 0
        self.game_over = False

        return self.get_state()


    def select_card(self, index):

        if self.game_over:
            return self.get_state()


        # Index invalid
        if index < 0 or index >= len(self.cards):
            return self.get_state()


        # Cartea este deja descoperită
        if index in self.revealed:
            return self.get_state()


        # Cartea a fost deja potrivită
        if index in self.matched:
            return self.get_state()


        self.revealed.append(index)


        # Așteptăm a doua carte
        if len(self.revealed) < 2:
            return self.get_state()


        self.attempts += 1

        first = self.revealed[0]
        second = self.revealed[1]


        # Pereche corectă
        if self.cards[first] == self.cards[second]:

            self.matched.extend([
                first,
                second
            ])

            self.score += 5

            self.revealed = []


            # Toate cărțile au fost găsite
            if len(self.matched) == len(self.cards):

                self.game_over = True


        # Pereche greșită
        else:

            pass


        return self.get_state()


    def hide_cards(self):

        if len(self.revealed) == 2:

            first = self.revealed[0]
            second = self.revealed[1]

            if self.cards[first] != self.cards[second]:

                self.revealed = []

        return self.get_state()


    def get_state(self):

        return {
            "cards": self.cards,
            "revealed": self.revealed,
            "matched": self.matched,
            "score": self.score,
            "attempts": self.attempts,
            "level": self.level,
            "game_over": self.game_over
        }