import socket
import sys
import threading
import json
from datetime import datetime
from keyboard import press

# Funktion för att öppna en socket och skapa en connection med server
def createConnection():
    IP, PORT = "172.16.117.80", 8080
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, PORT))
    return client, IP

# Funktion för att spara användarnamnet som sedan ska skickas in med protokollet
def createUsrn():
    my_username = input("Enter username: ")
    return my_username

#Funktion för att parsa/skapa en JSON sträng, detta blir då vårt protokoll som
#skickas till servern
def createJson(chatInput, client, IP, username):
    now = datetime.now()
    dt_str = now.strftime("%Y-%m-%d %H:%M:%S")
    currIp = client.getsockname()[0]

    jsobj = {
        "date":f"{dt_str}",
        "senderIP":f"{currIp}",
        "recipientIP":f"{IP}",
        "nickname":f"{username}",
        "message":f"{chatInput}"
        }
    jsonStr = json.dumps(jsobj)
    return jsonStr

#Funktion för att kunna ta emot meddelanden från servern
#Denna funktion körs som en egen tråd, för att kunna ta emot medd samtidigt
def recvMess(client):
    while True:
        from_server = client.recv(1024)
        if not from_server:
            print("Connection lost...")
            break
        print("\n\n", from_server.decode(encoding="utf-8", errors="strict"))
        press('enter')

#Detta är main-funktionen, behövs egentligen inte i python. Men skapade den för
#att exekvera koden på ett mer strukturerat sätt. Makes more sence to me!
def main():
    username = createUsrn()
    client, IP = createConnection()

    threading1 = threading.Thread(target=recvMess, args=(client,))
    threading1.daemon = True
    threading1.start()

    while True:
        chatInput = input(f"{username} > ")
        if chatInput:
            returnedJson = createJson(chatInput, client, IP, username)
            client.send(bytes(returnedJson, 'utf-8'))
            chatInput = None
        elif chatInput == "quit":
            sys.exit()

#Används för att kalla på Main, specifikt för python så att den vet att main körs primärt
if __name__ == "__main__":
    main()