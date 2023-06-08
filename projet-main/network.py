import socket

clients = []  # Liste des clients connectés

class Network:
    def __init__(self):
        # Création du socket
        self.interface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.110.14"  # Adresse IP du serveur
        self.port = 5555  # Port du serveur
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def getPos(self):
        return self.pos

    def connect(self):
        try:
            # Connexion au serveur
            self.interface.connect(self.addr)
            # Ajout de la connexion à la liste des clients du serveur
            clients.append(self.interface)
            # Réception de la position initiale du joueur depuis le serveur
            return self.interface.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            # Envoi des données au serveur
            self.interface.send(str.encode(data))
            # Réception de la réponse du serveur
            return self.interface.recv(2048).decode()
        except socket.error as e:
            print(e)
