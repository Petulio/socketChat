import socket
import threading
# 172.16.117.71
# 172.16.117.80
# 172.16.118.44
# grodvidar.xyz 1234
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('172.16.117.80', 8081))

def listen(lock):
    while True:
        from_server = client.recv(1024)
        if from_server != None:
            print ('From server: ', from_server.decode('utf-8'))
            from_server = None

lock = threading.Lock()
p = threading.Thread(target=listen, args=(lock,), daemon=True)
p.start()

while True:

    chatInput = input("Enter message: ")
    if chatInput != "":
        client.send(bytes(chatInput, 'utf-8'))
        chatInput = ""
    elif chatInput == "quit":
        break

client.close()