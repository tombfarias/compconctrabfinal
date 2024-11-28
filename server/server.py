import socket
import select
import sys
import os
import multiprocessing
import threading
import time
import queue

# Adiciona o caminho do diretório 'recursos' ao sys.path
recursos_path = os.path.join(os.path.dirname(__file__), '..', 'recursos')
if not os.path.isdir(recursos_path):
    raise ImportError(f"Diretório 'recursos' não encontrado no caminho: {recursos_path}")
sys.path.append(recursos_path)

from jogadores import Jogador
from jogo import Jogo

HOST = 'localhost'
PORT = 4004
TOTAL_JOGADORES = 10

class Server():
    def __init__(self):
        super().__init__()
        self.entradas = []
        self.jogadores = {}
        self.jogadoresEmEspera = queue.Queue()
        self.jogos = []
        self.msg_jogo = multiprocessing.Queue()

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((HOST, PORT))
        self.server.listen(TOTAL_JOGADORES)
        self.server.setblocking(True)
        self.entradas.append(self.server)


        # Para reconhecer o fim do programa
        self.fimProgramaR, self.fimProgramaW = socket.socketpair()
        self.entradas.append(self.fimProgramaR)


    def aceitaJogadores(self):
        try:
            clisock, endr = self.server.accept()
            # print(endr)
            self.jogadores[clisock] = Jogador(clisock, endr)
            self.jogadores[clisock].put_username()
            # self.entradas.append(clisock)
            print(f"Jogador: {self.jogadores[clisock].username}")
            self.jogadoresEmEspera.put(self.jogadores[clisock])
        except Exception as e:
            print(f"Erro ao aceitar jogador: {e}")

    def run(self):

        while True:
            try:
                # time.sleep(10)
                leitura, escrita, excecao = select.select(self.entradas, [], [])
                for pronto in leitura:
                    if pronto == self.fimProgramaR:
                        self.fimProgramaR.close()
                        self.fimProgramaW.close()
                        self.server.close()
                        exit(0)
                    elif pronto == self.server:
                        self.aceitaJogadores()
                        self.lobby()
                    
                    else:
                        try:
                            msg = pronto.recv(1024)
                            if msg == b'':
                                print(f"Conexão fechada pelo cliente: {pronto.getpeername()}")
                                self.entradas.remove(pronto)
                                pronto.close()
                            else:
                                print(f"Mensagem recebida: {msg}")
                        except Exception as e:
                            print(f"Erro ao receber do jogo: {e}")
                            self.entradas.remove(pronto)
                            pronto.close()
            except Exception as e:
                print(f"Erro no loop principal: {e}")
                exit(1)

            # Processar mensagens da fila
            while self.msg_jogo.qsize() > 0:
                msg = self.msg_jogo.get()
                print(f"Mensagem recebida do jogo: {msg}")

    def lobby(self):
        if self.jogadoresEmEspera.qsize() == 2:
            print("Lobby completo, iniciando jogo.")
            canalPai, canalFilho = multiprocessing.Pipe()

            jogador1 = self.jogadoresEmEspera.get()
            jogador2 = self.jogadoresEmEspera.get()
            novoJogo = Jogo(jogador1, jogador2, canalFilho).run()
            self.jogos.append(novoJogo)

            # Para escutar quando acabar o jogo
            threading.Thread(target=self.escutaJogo, args=(novoJogo, canalPai, )).start()
        else:
            for jogador in self.jogadoresEmEspera.queue:
                jogador.envia("Aguardando jogadores para iniciar o jogo.")

    def removerJogo(self, jogo):
        self.jogos.remove(jogo)
        print("Jogo encerrado.")

    def escutaFimServer(self):
        print("Digite 'fim' para encerrar o servidor.")
        while True:
            msg = input()
            if msg == "fim":
                self.encerrarServidor()


    def escutaJogo(self, jogo, canal):
        while True:
            try:
                msg = canal.recv()
                self.msg_jogo.append(msg)
                if msg == "FIM":
                    self.removerJogo(jogo)

            except Exception as e:
                print(f"Erro ao receber do jogo: {e}")
                break

    def encerrarServidor(self):

        # Terminar conexão com jogadores
        for jogador in self.jogadores.values():
            jogador.close()

        # Terminar conexão com jogos
        for jogo in self.jogos:
            jogo.close()

        # Encerrar servidor
        # Encerrar todos os processos
        self.fimProgramaW.send(b'fim')
        print("Servidor encerrado")

        exit(0)

if __name__ == "__main__":
    server = Server()
    print(f"Servidor iniciado e ouvindo na porta {PORT}")
    threading.Thread(target=server.escutaFimServer).start()
    server.run()