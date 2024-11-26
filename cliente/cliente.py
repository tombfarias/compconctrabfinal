import socket
import time


HOST = 'localhost'
PORT = 10001

class Cliente():
    def __init__(self):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

        self.username = ''

    def connect(self):
        while True:
            try:
                self.socket.connect((HOST, PORT))
                break
            except:
                print("Não foi possível conectar ao servidor. Tentando novamente em 5s...")
                time.sleep(5)


    def put_username(self):
        self.username = input("Digite seu username: ")
        self.socket.send(self.username.encode('utf-8'))


    def envia(self, msg):
        self.socket.send(msg.encode('utf-8'))
    
    def recebe(self, tam):
        return self.socket.recv(tam)
    
    def close(self):
        self.socket.close()
    

cliente = Cliente()
cliente.put_username()
print("Para sair digite 'fim'")
while True:
    # Trocar depois
    msg = input("Digite a sua jogada: ")
    if msg == 'fim': break
    cliente.envia(msg)
    msg = cliente.recebe(1024)
    print(str(msg, encoding='utf-8'))
    
