import socket
import sys
import threading
# 172.16.117.71
# 172.16.117.80
# 172.16.118.44
# grodvidar.xyz 1234
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("172.16.117.80", 8080))

threading1 = threading.Thread(target=recvMess)
threading1.daemon = True
threading1.start()

def recvMess():
    while True:
        from_server = client.recv(1024)
        print("Recieved: ", from_server)

while True:
    chatInput = input("Enter message: ")
    if chatInput != "":
        client.sendall(bytes(chatInput, 'utf-8'))
        chatInput = None
    elif chatInput == "quit":
        break

#  client.close()