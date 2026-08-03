import requests

class ServerClient:
    def __init__(self):
        self.server_ip = "127.0.0.1"
        self.server_port = 8000
        self.server_url = (
            f"http://{self.server_ip}:{self.server_port}"
        )

    def send_message(self, message):
        try:
            respone = requests.post(
                self.server_url + "/chat", json=message, timeout=5
            )
            return respone.json()
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }