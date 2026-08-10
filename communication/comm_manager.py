from Client.ServerClient import ServerClient
from activity.ActivityManager import ActivityManager


class ComunicationManager:

    def __init__(
        self,
        difficulty_manager,
        activity_manager
    ):

        self.difficulty_manager = difficulty_manager

        self.client = ServerClient()

        self.activity_manager = activity_manager


    def get_user_input(self):

        text = input("You: ")

        return text


    def build_request(self, text):

        message = {
            "text": text,
            "comm_level":
                self.difficulty_manager
                .get_current_comm_level()
        }

        return message


    def send_request(self, message):

        response = self.client.send_message(
            message
        )

        return response


    def process_text(self, text):

        self.activity_manager.reset_activity()

        request = self.build_request(
            text
        )

        response = self.send_request(
            request
        )

        return response


    def run(self):

        while True:

            text = self.get_user_input()

            response = self.process_text(
                text
            )

            print(response)