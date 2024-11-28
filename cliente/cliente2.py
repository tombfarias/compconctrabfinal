import socket
import time

import os
import sys
# Adiciona o caminho do diretório 'recursos' ao sys.path
recursos_path = os.path.join(os.path.dirname(__file__), '..', 'recursos')
if not os.path.isdir(recursos_path):
    raise ImportError(f"Diretório 'recursos' não encontrado no caminho: {recursos_path}")
sys.path.append(recursos_path)

from jogadores import Jogador
from jogo import Jogo

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
    
    def put_username(self):
        msg = cliente.recebe(1024)
        print(msg)
        if msg == "Digite seu username: ":
            msg = input()
            cliente.envia(msg)

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

    def jogada(self):
        #print("função jogada dentro de cliente2.py")
        jogada = input()
        self.envia(jogada)

    
    def run(self):
        while True:
            msg = self.recebe(1024)
            print(msg)
            if "Digite sua jogada: " in msg:
                #print("Mensagem correta enviada")
                self.jogada()
            elif "Jogada inválida. Tente novamente." in msg:
                    self.jogada() 
            elif "Você venceu!" in msg or "Você perdeu!" in msg or "Empate!" in msg:
                print(msg)
                break
            else:
                continue
    



if __name__ == "__main__":
    cliente = Cliente()
    cliente.put_username()

    cliente.run()

    
