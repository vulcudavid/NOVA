from communication.comm_manager import ComunicationManager
from difficulty.difficulty_manager import DifficultyManager

difficulty = DifficultyManager()

manager = ComunicationManager(difficulty)

manager.run()