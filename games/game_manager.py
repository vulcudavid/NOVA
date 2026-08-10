from games.MemoryGame import MemoryGame


class GameManager:

    def __init__(self, difficulty_manager):

        self.memory_game = MemoryGame()
        self.difficulty_manager = difficulty_manager


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