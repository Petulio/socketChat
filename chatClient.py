import socket
import sys
import threading
import json
from datetime import datetime
from keyboard import press

# grodvidar.xyz 1234

def createConnection():
    IP, PORT = "192.168.156.54", 8080
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, PORT))
    return client, IP

def createUsrn():
    my_username = input("Enter username: ")
    return my_username

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

def recvMess(client):
    while True:
        from_server = client.recv(1024)
        if not from_server:
            print("Connection lost...")
            break
        print("\n\nRecieved:", from_server.decode(encoding="utf-8", errors="strict"))
        press('enter')


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

if __name__ == "__main__":
    main()