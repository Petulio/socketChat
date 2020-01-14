import socket
import sys
import threading
import json
from datetime import datetime
from keyboard import press
# 172.16.117.71
# 172.16.117.80
# 172.16.118.44
# grodvidar.xyz 1234
IP, PORT = "127.0.0.1", 8080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))
my_username = input("Enter username: ")

def createJson(chatInput):
    now = datetime.now()
    dt_str = now.strftime("%Y-%m-%d %H:%M:%S")
    currIp = socket.gethostbyname(socket.gethostname())

    jsobj = {
        "date":f"{dt_str}",
        "senderIP":f"{currIp}",
        "recipientIP":f"{IP}",
        "nickname":f"{my_username}",
        "message":f"{chatInput}"
        }
    jsonStr = json.dumps(jsobj)
    return jsonStr

def recvMess():
    while True:
        from_server = client.recv(1024)
        if not from_server:
            print("Connection lost...")
            break
        print("\n\nRecieved: ", from_server)
        press('enter')

threading1 = threading.Thread(target=recvMess)
threading1.daemon = True
threading1.start()

while True:
    chatInput = input(f"{my_username} > ")
    if chatInput:
        returnedJson = createJson(chatInput)
        client.send(bytes(returnedJson, 'utf-8'))
        chatInput = None
    elif chatInput == "quit":
        sys.exit()
