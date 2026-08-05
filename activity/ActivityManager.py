import time
import random


class ActivityManager:

    def __init__(self):

        self.last_activity = time.time()

        self.timeout = 600        # 10 minute

        self.messages = [

            "Salut! Mai ești aici?",

            "Dacă ai nevoie de mine, sunt aici.",

            "Vrei să continuăm?",

            "Putem continua când dorești.",

            "Dacă vrei, putem încerca și un joc."

        ]

    def reset_activity(self):

        self.last_activity = time.time()

    def is_timeout(self):

        current_time = time.time()

        return (current_time - self.last_activity) >= self.timeout

    def get_message(self):

        self.reset_activity()

        return random.choice(self.messages)