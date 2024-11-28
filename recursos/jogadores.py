import socket
import time

class Jogador():
    def __init__(self, socket, endereco):
        self.username = ''
        self.socket = socket
        self.endereco = endereco
        self.peca = 0

    def __str__(self):
        return self.username
    
    def envia(self, msg):
        self.socket.send(msg.encode('utf-8'))
    
    def recebe(self, tam):
        while True:
            try:
                #print("self.socketrcv")
                retorno = self.socket.recv(tam).decode('utf-8')
                #print("jogada recebida é", retorno)
                return retorno
            except socket.error as e:
                if e.errno == 10035:
                    continue
                else:
                    raise e
    
    def put_username(self):
        self.envia("Digite seu username: ")
        while True:
            try:
                self.username = self.recebe(1024)
                if self.username:
                    break
            except Exception as e:
                time.sleep(2)
                continue

    
    def get_endereco(self):
        return self.endereco
        
        
    def joga(self):
        self.envia("Digite sua jogada: ")
        #print("Abaixo do digite sua jogada")
        while True:
            #print("entrei no while")
            try:
                #print("ENTREI NO TRY")
                retorno = self.recebe(1024)
                print("recebido")
                return retorno
            except Exception as e:
                print("Entrei no Except")
                time.sleep(2)
                continue


