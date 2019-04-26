# Auteurs: Benjamin BEYERLE - Philippe DA SILVA OLIVEIRA
# Classe: SRC1 - 3E

#importation des modules nécessaires
import socket
import select
 
# Les paramètres du serveur
hote = '127.0.0.1'
port = 5000


# Fonction pour broadcasté les messages à tous les clients connectés
def broadcast_data (sock, message):
    # Ne pas envoyer le message à l'expediteur
    for socket in clients_connectes:
        if socket != server_socket and socket != sock:
            try:
                socket.send(bytes(message, 'utf-8'))
            except socket.error:
                socket.close()
                clients_connectes.remove(socket)


# Définition du socket de connexion
connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(5)

print("Le serveur écoute à présent sur le port :", port)
 
serveur_lancé = True  #booléen

# liste de clients suceptibles de solliciter le serveur
clients_connectes = []

while serveur_lancé:  ## while True:
    # On va vérifier les nouveaux clients qui se connectent
    # Pour cela, on écoute la connexion_principale en lecture
    # On attend maximum 50ms
    connexions_demandees, wlist, xlist = select.select([connexion_principale], [], [], 0.06)  # 60 ms de time out
     
    for connexion in connexions_demandees:  # les clients  de rlist
        connexion_avec_client, infos_connexion = connexion.accept()

        # Renvoi du socket du client accepté
        # On ajoute le socket connecté à la liste des clients
        clients_connectes.append(connexion_avec_client)
     
    # On écoute la liste des clients connectés
    # Les clients renvoyés par select sont ceux devant être lus (recv)
    # On attend là  50ms maximum
    # On encadre l'appel à select.select dans un bloc try
    # En effet, si la liste de clients connectés est vide, une exception
    # Peut être levée

    ### Autre scénario 

    clients_a_lire = []
    try:
        clients_a_lire, wlist, xlist = select.select(clients_connectes, [], [], 0.05)
    except select.error:
        pass

#on continue en séquence si pas d'erreurs
    else:  
           # On parcourt la liste des clients à lire
        for client in clients_a_lire:
            # Client est de type socket
            msg_recu = client.recv(1024)
            msg_recu = msg_recu.decode()
            if msg_recu.startswith('username='):
                print('1')
                new = msg_recu.replace('username= ', '')
                msg_recu = new
                print(msg_recu)
                msg_recu = msg_recu + ' à rejoint le chat.'
            print("Message reçu du client ", client.getpeername(), " : ", msg_recu)
            for client_broadcast in clients_connectes:
                print(client_broadcast.getpeername())

                if client_broadcast != client:
                    print('Sending message')
                    client_broadcast.send(bytes(msg_recu, 'utf-8'))

            if msg_recu.upper() == "FIN":
                serveur_lance = False

              
print("Fermeture des connexions par l'un des clients ")

# Fermeture des connexions donc des sockets
for client in clients_connectes:
    client.close()
 
connexion_principale.close()  ## Fermeture du socket principal
