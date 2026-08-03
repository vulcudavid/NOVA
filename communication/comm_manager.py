class ComunicationManager:

    def __init__(self, difficulty_manager): #se initializeaza dificultatea, textul si obiectul de tip client
        self.difficulty_manager = difficulty_manager
        self.client = ServerClient()  # se defineste ServerClient in aplta parte

    def get_user_input(self): #se preia inputul dat de utilizator si se returneaza textul
        text = input("You: ")
        return text

    def build_request(self, text): #se construieste un mesaj care contine textul si nivelul de dificultate curent, apoi se returneaza mesajul
        message = {
            "text": text,
            "comm_level": self.difficulty_manager.get_current_comm_level()
        }
        return message

    def send_request(self, message): #se trimite mesajul si se returneaza raspunsul
        response = self.client.send_message(message)
        return response

    def run(self): #se ruleaza bucla principala a aplicatiei
        while True:
            text = self.get_user_input()
            request = self.build_request(text)
            response = self.send_request(request)
            print(response)