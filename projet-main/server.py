import socket
from _thread import *
import sys

# Adresse IP du serveur
server = "192.168.110.1"  # Remplacez par votre propre adresse IP, ex : "192.168.0.100"

# Port d'écoute du serveur
port = 5555

# Création du socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Liaison du socket à l'adresse IP et au port
    s.bind((server, port))
except socket.error as e:
    str(e)

# Nombre maximal de connexions simultanées
s.listen(4)

# Message indiquant que le serveur est en attente de connexions
print("Waiting for a connection. Server Started")

# Positions des joueurs
pos = [(0, 0), (100, 100)]

# Fonction exécutée dans un thread pour gérer la communication avec un client
def threaded_interface(conn, player):
    # Envoi de la position initiale du joueur au client
    conn.send(str.encode(make_pos(pos[player])))

    while True:
        try:
            # Réception des données du client
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data

            if not data:
                # Si aucune donnée n'est reçue, le client est déconnecté
                print("Disconnected")
                break
            else:
                if player == 1:
                    # Si c'est le joueur 1, envoyer la position du joueur 0 à tous les clients
                    reply = pos[0]
                else:
                    # Si c'est le joueur 0, envoyer la position du joueur 1 à tous les clients
                    reply = pos[1]
                print("Received:", data)
                print("Sending:", reply)

                # Envoi de la position mise à jour à tous les clients
                for c in clients:
                    c.sendall(str.encode(make_pos(reply)))
        except:
            break

    # Fermeture de la connexion en cas de perte de connexion avec le client
    print("Lost connection")
    conn.close()


# Numéro de joueur en cours
concurrentPlayer = 0

clients = []
while True:
    # Attente d'une connexion entrante
    conn, addr = s.accept()
    print("Connected to:", addr)

    # Ajout de la connexion à la liste des clients
    clients.append(conn)

    # Démarrage d'un nouveau thread pour gérer la connexion avec le client
    start_new_thread(threaded_interface, (conn, concurrentPlayer))

    # Incrémentation du numéro de joueur pour la prochaine connexion
    concurrentPlayer += 1


    def make_pos(pos):
        return str(pos[0]) + "," + str(pos[1])

