import time

class DifficultyManager:
    def __init__(self):
        self.happy_start = None
        self.sadAngry_start = None
        self.current_score=50
        self.last_change_message = ""
        self.currentComm_level = 1
        self.currentGame_level = 1

    def emotion_manager(self, emotion, confidence):
        if emotion == "happy" and confidence >= 0.8:
            if self.happy_start is None:
                self.happy_start = time.monotonic()
            elapsed_time = time.monotonic() - self.happy_start
            if elapsed_time >= 20:
                self.increase_comm_difficulty()
                self.happy_start = None
        else:
            self.happy_start = None

        if emotion in ["sad", "angry"] and confidence >= 0.8:
            if self.sadAngry_start is None:
                self.sadAngry_start = time.monotonic()
            elapsed_time = time.monotonic() - self.sadAngry_start
            if elapsed_time >= 20:
                self.decrease_comm_difficulty()
                self.sadAngry_start = None
        else:
            self.sadAngry_start = None

    def score_manager(self, score):
        self.current_score = max(0, min(score, 100))

    def increase_game_difficulty(self):
        if self.currentGame_level < 3:
            self.currentGame_level += 1
            self.last_change_message = "Difficulty Increased!"

    def decrease_game_difficulty(self):
        if self.currentGame_level > 1:
            self.currentGame_level -= 1
            self.last_change_message = "Difficulty Decreased!"

    def increase_comm_difficulty(self):
        if self.currentComm_level < 3:
            self.currentComm_level += 1

    def decrease_comm_difficulty(self):
        if self.currentComm_level > 1:
            self.currentComm_level -= 1

    
    def get_current_comm_level(self):
        return self.currentComm_level

    def get_current_game_level(self):
        return self.currentGame_level

    def add_score(self, points):
        self.current_score += points
        self.score_manager(self.current_score)

    def get_score(self):
        return self.current_score

    def should_increase_game(self):
        return self.current_score >= 80

    def should_decrease_game(self):
        return self.current_score <= 20