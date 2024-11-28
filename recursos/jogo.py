import multiprocessing
from tabuleiro import tab_P, tab_G, conv

class Jogo(multiprocessing.Process):
    def __init__(self, jogador1, jogador2, canal):
        super().__init__()
        self.set_jogadores(jogador1, jogador2)
        self.tabuleiro = tab_G()
        self.escolhe_tab = True

        self.canal = canal

    def enviar(self, mensagem):
        self.canal.send(mensagem.encode())

    def enviarVencedor(self, jogador):
        self.enviar(f"O jogador {jogador.username} venceu!")

    def enviarEmpate(self):
        self.enviar("O jogo terminou empatado!")

    def requisitarJogada(self, jogador):
        jogador.enviar("Digite a sua jogada: ")
        return jogador.recebe(1024)
    
    def requisitarJogadaInvalida(self, jogador):
        jogador.enviar("Jogada inválida. Tente novamente: ")
        return jogador.recebe(1024)

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
        troca = True
        tabP_atual = None


        while self.tabuleiro.encerradas < 9: #enquanto o jogo grande não acabar, continua
            # Cada rodada é uma iteração do loop

            # clear a cada rodada
            self.jogador1.envia("clear")
            self.jogador2.envia("clear")

            self.jogador1.envia(self.tabuleiro.toString())
            self.jogador2.envia(self.tabuleiro.toString())
            if troca:
                if jogador_atual == self.jogador1:
                    jogador_atual = self.jogador2
                else:
                    jogador_atual = self.jogador1
            
            # print(f"Jogador atual: {jogador_atual.username}")
            # print(f"escolhe_tab: {self.escolhe_tab}")

            # if self.escolhe_tab: #se for a primeira jogada ou for enviado pra um tabuleiro já encerrado
                # jogador_atual.envia("Digite a sua jogada: ")
                # A = jogador_atual.recebe(1024)
                # if A.upper() == "FIM":
                    # print("Jogo encerrado")
                    # break
                # A = conv('G', A, jogador_atual)
                #tratar o A pra ser entrada

            if tabP_atual == None:
                # Pedir para o jogador escoher onde irá jogar
                jogada = self.tabuleiro.movimentoG(jogador_atual) 
            else:
                jogada = self.tabuleiro.movimentoG(jogador_atual, tabP_atual)


            

            #if jogada == 10: #tab_pequeno encerrado
                #self.escolhe_tab = True
               # troca = False
                
                #continue
          #  if jogada == 11: #Movimento inválido dentro do tab_pequeno
            #    self.escolhe_tab = False
           #     troca = False
           #     continue
           # else:
             #   A = jogada
            #    print(f"Jogada feita: {A}")
            #    self.escolhe_tab = False
           #     troca = True
            #if self.tabuleiro.encerradas == 9:
                #break
            
        return self.tabuleiro.fim()
    
    def close(self):
        self.canal.close()
        self.terminate()
        self.join()


    def run(self):
        self.start()
        self.canal.close()


export = Jogo