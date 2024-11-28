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
                print("Conectando ao servidor...", self.socket.getpeername())
                break
            except Exception as e:
                print(f"Erro: {e}. Tentando novamente em 5s...")
                time.sleep(5)
    
    def put_username(self):
        msg = cliente.recebe(1024)
        print(msg)
        if msg == "Digite seu username: ":
            msg = input()
            cliente.envia(msg)

    def envia(self, msg):
        self.socket.send(msg.encode('utf-8'))
    
    def recebe(self, tam):
        msg = ''
        try:
            msg = self.socket.recv(tam).decode('utf-8')
            if msg == '':
                print("Conexão fechada pelo servidor.")
                self.close()
                exit(1)
            
        except socket.error as e:
            print(f"Erro ao receber dados: {e}")
            self.close()
            exit(1)
                

        return msg
    
    def close(self):
        self.socket.close()

    def jogada(self):
        jogada = input()
        self.envia(jogada)

    
    def run(self):
        while True:
            msg = self.recebe(1024)
            print(msg)
            time.sleep(1)
            if msg == "Digite sua jogada: " or "Jogada inválida. Tente novamente: ":
                self.jogada()
            elif msg == "Você venceu!" or msg == "Você perdeu!" or msg == "Empate!":
                break
            else:
                continue
    



if __name__ == "__main__":
    cliente = Cliente()
    cliente.put_username()

    cliente.run()

    
