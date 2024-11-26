import socket
import select
import sys
import os
import multiprocessing
import queue

# Adiciona o caminho do diretório 'recursos' ao sys.path
recursos_path = os.path.join(os.path.dirname(__file__), '..', 'recursos')
if not os.path.isdir(recursos_path):
    raise ImportError(f"Diretório 'recursos' não encontrado no caminho: {recursos_path}")
sys.path.append(recursos_path)


from jogadores import Jogador
from jogo import Jogo


HOST = 'localhost'
PORT = 10001
TOTAL_JOGADORES = 10
class Server ():
    def __init__(self):
        super().__init__()
        self.entradas = [sys.stdin]
        self.jogadores = {}
        self.jogadoresEmEspera = queue.Queue()
        self.jogos = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))

        
        self.server.setblocking(False)
        self.entradas.append(self.server)

    def aceitaJogadores(self):
        clisock, endr = self.server.accept()
        self.jogadores[clisock] = Jogador(clisock, endr)
        self.jogadores[clisock].put_username()
        self.jogadoresEmEspera.put(self.jogadores[clisock])
    
    def run(self):
        while True:
            # Espera por jogadores
            leitura, escrita, excecao = select.select(self.entradas, [], [])
            for pronto in leitura:
                if pronto == sys.stdin:
                    break
                elif pronto == self.server:
                    self.aceitaJogadores()
                    self.lobby()
                else:
                    continue
          

    
 
    
    def lobby(self):
        if self.jogadoresEmEspera.qsize() == 2:
            
            # Criar canal entre o servidor e o jogo
            
            canalPai,canalFilho = multiprocessing.Pipe()
            novoJogo = Jogo(self.jogadoresEmEspera.get(), self.jogadoresEmEspera.get(), canalFilho)
            self.jogos.append(novoJogo)

            # Para escutar quando acabar o jogo
            self.entradas.append(canalPai)

            self.start()


server = Server()
server.run()

        

            
    




    