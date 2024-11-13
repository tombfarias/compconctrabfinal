import socket
import select
import sys
import multiprocessing

import queue


from recursos.jogo import Jogo
from recursos.jogadores import Jogador

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

        self.listen(TOTAL_JOGADORES)
        self.server.setblocking(False)

        self.entradas.append(self.server)

    def aceitaJogadores(self):
        clisock, endr = self.server.accept()
        self.jogadores[clisock] = endr
        return clisock, endr
    
    def lobby(self):
        if self.jogadoresEmEspera.qsize() == 2:
            
            # Criar canal entre o servidor e o jogo
            
            canalPai,canalFilho = multiprocessing.Pipe()
            novoJogo = Jogo(self.jogadoresEmEspera.get(), self.jogadoresEmEspera.get(), canalFilho)
            self.jogos.append(novoJogo)

            # Para escutar quando acabar o jogo
            self.entradas.append(canalPai)

            self.start()
        
        

            
    




    