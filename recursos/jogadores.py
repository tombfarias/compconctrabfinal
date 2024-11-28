import time

class Jogador():
    def __init__(self, socket, endereco):
        self.username = ''
        self.socket = socket
        self.endereco = endereco

    def __str__(self):
        return self.username
    
    def envia(self, msg):
        self.socket.send(msg.encode('utf-8'))
    
    def recebe(self, tam):
        msg = ''
        while True:
            try:
                msg = self.socket.recv(tam).decode('utf-8')
                if msg == 'ping':
                    self.envia('pong')
                    continue
                break
            except OSError as e:
                if e.errno == 10035:
                    time.sleep(3)
                    continue
                else:
                    raise e
        
        return msg
    
    def put_username(self):
        self.envia("Digite seu username: ")
        while True:
            try:
                self.username = self.recebe(1024)
                ############################
                if self.username:
                    break
            except Exception as e:
                time.sleep(2)
                continue
    

    def close(self):
        self.socket.close()
    
    def get_endereco(self):
        return self.endereco
    
    def escutarJogador(self):
        while True:
            try:
                msg = self.recebe(1024)
                if msg == '':
                    print(f"Conexão fechada pelo cliente: {self.socket.getpeername()}")
                    self.close()
                    return
                else:
                    print(f"Mensagem recebida: {msg}")
            except Exception as e:
                print(f"Erro ao receber do jogo: {e}")
                self.close()
                return
        
        