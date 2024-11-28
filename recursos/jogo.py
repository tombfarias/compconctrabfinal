import multiprocessing
from tabuleiro import tab_P, tab_G, conv

class Jogo(multiprocessing.Process):
    def __init__(self, jogador1, jogador2, canal):
        super().__init__()
        jogador1.peca = 'X'
        jogador2.peca = 'O'
        self.set_jogadores(jogador1, jogador2)
        self.tab_P = tab_P()
        self.tabuleiro = tab_G()

        self.canal = canal

    def enviarVencedor(self, jogador):
        self.canal.send(f"O jogador {jogador.username} venceu!".encode())

    def enviarEmpate(self):
        self.canal.send("O jogo terminou empatado!".encode())




    def set_jogadores(self, jogador1, jogador2):
        self.jogador1 = jogador1
        self.jogador2 = jogador2


    def get_jogadores(self):
        return self.jogador1, self.jogador2
    
    def get_jogadores(self, username):
        if self.jogador1.username == username:
            return self.jogador1
        elif self.jogador2.username == username:
            return self.jogador2

        return None
    

    
    
    def start(self):
        jogador_atual = self.jogador2
        #print(type(jogador_atual))
        troca = True
        escolhe = True
        while self.tabuleiro.encerradas < 9: #enquanto o jogo grande não acabar, continua
            self.tabuleiro.print(self.jogador1, self.jogador2)
            print(self.tabuleiro.placar1)
            #print()
            #print(self.tabuleiro.placar2)
            
            if troca:
                if jogador_atual == self.jogador1:
                    jogador_atual = self.jogador2
                else:
                    #print(type(jogador_atual))
                    jogador_atual = self.jogador1
                    #print(type(jogador_atual))
                
            if escolhe: #se for a primeira jogada ou for enviado pra um tabuleiro já encerrado
                #print("jogador atual é um", type(jogador_atual))

                #A = jogador_atual.joga()
                jogador_atual.envia("Jogada tab grande\n")
                A = jogador_atual.joga()
                if "FIM" in A.upper():
                    print("Jogo encerrado")
                    break
                A = conv('G', A, jogador_atual)
                #tratar o A pra ser entrada
            jogada = self.tabuleiro.movimentoG(A, jogador_atual) 
            if jogada == 10: #tab_pequeno encerrado
                escolhe= True
                troca = False
                
                continue
            if jogada == 11: #Movimento inválido dentro do tab_pequeno
                escolhe = False
                troca = False
                continue
            else:
                A = jogada
                print("jogada feita")
                escolhe = False
                troca = True
            #if self.tabuleiro.encerradas == 9:
                #break
            
        return self.tabuleiro.fim()
                


    def run(self):
        self.start()
        self.canal.close()


export = Jogo
