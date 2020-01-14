import socketserver

class myTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            self.data = self.request.recv(1024).strip()
            if not self.data:
                break
            print("{} wrote:".format(self.client_address[0]))
            print(self.data)
            self.request.send(self.data.upper())

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    with socketserver.TCPServer((HOST, PORT), myTcpHandler) as server:
        server.serve_forever()