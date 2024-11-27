import socket
import time


HOST = 'localhost'
PORT = 3001

class Cliente():
    def __init__(self):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = ''
        self.connect()

    def connect(self):
        while True:
            try:
                self.socket.connect((HOST, PORT))
                print("Conectando ao servidor...")
                break
            except Exception as e:
                print(f"Erro: {e}. Tentando novamente em 5s...")
                time.sleep(5)


    def envia(self, msg):
        self.socket.send(msg.encode('utf-8'))
    
    def recebe(self, tam):
        while True:
            try:
                return self.socket.recv(tam).decode('utf-8')
            except socket.error as e:
                if e.errno == 10035:
                    continue
                else:
                    raise e
    
    def close(self):
        self.socket.close()
    

if __name__ == "__main__":
    cliente = Cliente()
