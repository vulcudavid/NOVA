import requests


class ServerClient:

    def __init__(self):

        self.server_url = "http://192.168.100.84:8000/chat"

    def send_message(self, message):

        try:

            response = requests.post(
                self.server_url,
                json=message
            )

            return response.json()

        except Exception as e:

            return {
                "error": str(e)
            }