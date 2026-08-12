from games.MemoryGame import MemoryGame
from games.ReactionGame import ReactionGame


class GameManager:

    def __init__(self, difficulty_manager):

        self.memory_game = MemoryGame()
        self.reaction_game = ReactionGame()
        self.difficulty_manager = difficulty_manager

        # Statistici Memory Game
        self.memory_games_played = 0
        self.memory_best_score = 0
        self.memory_total_score = 0

        # Statistici Reaction Game
        self.reaction_games_played = 0
        self.reaction_best_time = float('inf')
        self.reaction_total_time = 0
        self.reaction_best_score = 0


    def start_memory(self, level=None):

        if level is None:
            level = self.difficulty_manager.get_current_game_level()

        return self.memory_game.start(level)

    def memory_input(self, index):

        old_score = self.memory_game.score

        state = self.memory_game.select_card(index)

        new_score = self.memory_game.score

        score_difference = new_score - old_score

        if score_difference != 0:

            self.difficulty_manager.add_score(
                score_difference
            )

        return self.get_memory_state_with_difficulty()

    def get_memory_state_with_difficulty(self):

        state = self.memory_game.get_state()

        state["global_score"] = self.difficulty_manager.get_score()
        state["game_level"] = self.difficulty_manager.get_current_game_level()

        state["can_increase_level"] = (
            self.difficulty_manager.should_increase_game()
        )

        state["can_decrease_level"] = (
            self.difficulty_manager.should_decrease_game()
        )

        state["level_message"] = (
            self.difficulty_manager.last_change_message
        )

        return state


    def memory_hide(self):

        return self.memory_game.hide_cards()


    def get_memory_state(self):

        return self.memory_game.get_state()

    def increase_game_level(self):

        self.difficulty_manager.increase_game_difficulty()


    def decrease_game_level(self):

        self.difficulty_manager.decrease_game_difficulty()


    # ============================================================
    # REACTION GAME
    # ============================================================

    def start_reaction(self):

        return self.reaction_game.start()


    def get_reaction_state(self):

        state = self.reaction_game.check_ready()

        return state


    def reaction_input(self):

        old_score = self.reaction_game.score

        state = self.reaction_game.react()

        new_score = self.reaction_game.score

        if new_score > 0:

            self.difficulty_manager.add_score(
                new_score
            )

            # Actualizez statistici
            if self.reaction_game.game_over:

                self.reaction_games_played += 1

                reaction_time = self.reaction_game.reaction_time

                self.reaction_total_time += reaction_time

                if reaction_time < self.reaction_best_time:

                    self.reaction_best_time = reaction_time

                if new_score > self.reaction_best_score:

                    self.reaction_best_score = new_score

        return state


    # ============================================================
    # STATISTICS
    # ============================================================

    def update_memory_stats(self):

        """Actualizez statistici după ce memoria se termină"""

        if self.memory_game.game_over:

            self.memory_games_played += 1

            current_score = self.memory_game.score

            self.memory_total_score += current_score

            if current_score > self.memory_best_score:

                self.memory_best_score = current_score


    def get_settings(self):

        """Returnez setările și statisticile pentru settings page"""

        self.update_memory_stats()

        avg_memory_score = (
            self.memory_total_score / self.memory_games_played
            if self.memory_games_played > 0
            else 0
        )

        avg_reaction_time = (
            self.reaction_total_time / self.reaction_games_played
            if self.reaction_games_played > 0
            else 0
        )

        return {
            "comm_level": self.difficulty_manager.get_current_comm_level(),
            "game_level": self.difficulty_manager.get_current_game_level(),
            "current_score": self.difficulty_manager.get_score(),
            "memory": {
                "games_played": self.memory_games_played,
                "best_score": self.memory_best_score,
                "average_score": round(avg_memory_score, 2)
            },
            "reaction": {
                "games_played": self.reaction_games_played,
                "best_time": round(self.reaction_best_time, 2) if self.reaction_best_time != float('inf') else 0,
                "average_time": round(avg_reaction_time, 2),
                "best_score": self.reaction_best_score
            }
        }