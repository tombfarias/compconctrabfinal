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
PORT = 3001
TOTAL_JOGADORES = 10
class Server ():
    def __init__(self):
        super().__init__()
        self.entradas = []
        self.jogadores = {}
        self.jogadoresEmEspera = queue.Queue()
        self.jogos = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((HOST, PORT))
        self.server.listen(TOTAL_JOGADORES)
        self.server.setblocking(False)
        self.entradas.append(self.server)

    def aceitaJogadores(self):
        try:
            clisock, endr = self.server.accept()
            print(f"Jogador aceito: {endr}")
            self.jogadores[clisock] = Jogador(clisock, endr)
            self.jogadores[clisock].put_username()
            self.jogadoresEmEspera.put(self.jogadores[clisock])
        except Exception as e:
            print(f"Erro ao aceitar jogador: {e}")
    
    def run(self):
        while True:
            # Espera por jogadores
            try:
                leitura, escrita, excecao = select.select(self.entradas, [], [], 1.0)
                for pronto in leitura:
                    if pronto == self.server:
                        self.aceitaJogadores()
                        self.lobby()
                    else:
                        try:
                        # Verifica se o canalPai está pronto para leitura
                            msg = pronto.recv(1024)
                            if msg == b'':
                                self.entradas.remove(pronto)
                                pronto.close()
                            else:
                                print(f"Recebi do jogo: {msg}")
                        except Exception as e:
                            print(f"Erro ao receber do jogo: {e}")
                            self.entradas.remove(pronto)
                            pronto.close()

            except Exception as e:
                print(f"Erro no loop principal: {e}")
                exit(1)
          

    
    def lobby(self):
        if self.jogadoresEmEspera.qsize() == 2:
            print("Lobby completo, iniciando jogo.")
            # Criar canal entre o servidor e o jogo
           
            canalPai, canalFilho = multiprocessing.Pipe()
            novoJogo = Jogo(self.jogadoresEmEspera.get(), self.jogadoresEmEspera.get(), canalFilho)
            self.jogos.append(novoJogo)

            # Para escutar quando acabar o jogo
            self.entradas.append(canalPai)

    def encerrarServidor(self):
        for jogador in self.jogadores:
            jogador.close()
        self.server.close()
        exit(0)




if __name__ == "__main__":
    server = Server()
    print(f"Servidor iniciado e ouvindo na porta {server.server.getsockname()[1]}")
    server.run()

        

            
    




    