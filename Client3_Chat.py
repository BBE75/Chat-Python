# Auteurs: Benjamin BEYERLE - Philippe DA SILVA OLIVEIRA
# Classe: SRC1 - 3E

import socket
import sys
import threading
import time


# Fonction d'écoute pour le thread
def recvMessage():
    while True:
        msgServer = sock.recv(1024)
        if not msgServer:
            sys.exit(0)
        print(msgServer.decode())


# création d'un socket pour la connexion avec le serveur en local
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # connexion au serveur, bloc surveillé, et gestion de l'exception
    sock.connect(('127.0.0.1', 5000))

except socket.error:
   print("la connexion a échoué.......")
   sys.exit()
# Saisie du username
username = input("Choisissez votre nom d'utilisateur: ")

print(">>> Connexion établie avec le serveur...")
# Envoi du username avec un tag particulier pour etre gérer par le serveur
sock.send(bytes('username= '+username, 'utf-8'))

# Démarrage du thread pour la fonction d'écoute afin de recevoir les messages instantanement
p2 = threading.Thread(target=recvMessage)
p2.start()

# Boucle pour la saisie des messages, on tag le username sur le message afin de l'afficher aux autres clients
msgClient = b""
while msgClient.upper() != b"FIN":

    msgClient = input()
    msgClient = '<' + username + '>: ' + msgClient
    msgClient = msgClient.encode()
    sock.send(msgClient)

print(" Fermeture de ma connexion ")
sock.close()
