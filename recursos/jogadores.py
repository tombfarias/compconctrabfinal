import socket
import select
import sys
import multiprocessing

class Jogador():
    def __init__(self, socket, endereco):
        self.username = ''
        self.socket = socket
        self.endereco = endereco

    def __str__(self):
        return self.username
    
    def envia(self, msg):
        self.socket.send(msg)
    
    def recebe(self, tam):
        return self.socket.recv(tam)
    
    def put_username(self):
        self.envia("Digite seu username: ")
        self.username = self.recebe(1024)

    
    def get_endereco(self):
        return self.endereco
        
        