import socket
import time
import os
import select
import threading

HOST = 'localhost'
PORT = 4004

class Cliente():
    def __init__(self):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socketPing = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.username = ''
        self.connect(self.socket)
        # self.connect(self.socketPing)
        self.entradas = [self.socket]

        # self.thread = threading.Thread(target=self.verificarConexaoAindaAtiva)


    def verificarConexaoAindaAtiva(self):
        """
        Thread que ecoa para servidor para verificar se a conexão ainda está ativa
        """
        while True:
            time.sleep(10)
            self.envia(self.socketPing, 'ping')       
            leitura, _, _ = select.select([self.entradas], [], [], 15)
            if leitura:
                for pronto in leitura:
                    if pronto == self.socket:
                        try:
                            msg = self.recebe(self.socketPing, 1024)
                            if msg == '':
                                self.conexaoFechada()
                                return
                        except Exception as e:
                            self.conexaoFechada()
                            return






    def connect(self, socket):
        while True:
            try:
                socket.connect((HOST, PORT))
                print("Conectando ao servidor...", socket.getpeername())

                break
            except Exception as e:
                print(f"Erro: {e}. Tentando novamente em 5s...")
                time.sleep(5)
    
    def put_username(self):
        msg = self.recebe(self.socket, 1024)
        print(msg)
        if msg == "Digite seu username: ":
            msg = self.inputJogador()
            self.envia(self.socket, msg)

    def envia(self, socket, msg):
        try:
            socket.send(msg.encode('utf-8'))
        except Exception as e:
            self.conexaoFechada()

    def conexaoFechada(self):
        print("Conexão fechada pelo servidor.")
        self.close()
    
    def recebe(self, socket, tam):
        msg = ''
        try:
            msg = socket.recv(tam).decode('utf-8')
            if msg == '':
                self.conexaoFechada()
            
        except OSError as e:
            self.conexaoFechada()
            self.close()
                
        return msg
    
    def close(self):
        self.socket.close()
        # self.socketPing.close()
        exit(1)

    def jogadaValida(self, jogada):

        if len(jogada) != 2:
            return False
        if not jogada[0].isdigit() or not jogada[1].isdigit():
            return False
        if int(jogada[0]) not in range(1, 4) or int(jogada[1]) not in range(1, 4):
            return False
        return True

    def inputJogador(self):
        mensagem = input()
        if mensagem == 'fim':
            self.close()
        return mensagem

    def jogada(self):
        jogada = self.inputJogador()
        # Validar jogada (a jogada dever ser uma string de tam 2 contendo 2 numeros de [1 a 3])
        while not self.jogadaValida(jogada):
            print("Jogada inválida. Tente novamente: ")
            jogada = self.inputJogador()
        
        jogada = str(int(jogada[0]) - 1) + str(int(jogada[1]) - 1)
        self.envia(self.socket, jogada)

    
    def run(self):
        while True:
            msg = self.recebe( self.socket, 1024)
            if msg == 'clear':
                self.clear()
                continue
            print(msg)
            time.sleep(1)
            if ':' in msg:
                self.jogada()
            elif msg == "Você venceu!" or msg == "Você perdeu!" or msg == "Empate!":
                break
            else:
                continue

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    



if __name__ == "__main__":
    cliente = Cliente()
    
    cliente.put_username()
    cliente.run()

    
