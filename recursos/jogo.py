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
    

    def outroJogador(self, jogador1, jogador2, jogadorAtual):
        if jogadorAtual == jogador1:
            return jogador2
        return jogador1
    
    def start(self):
        jogador_atual = self.jogador2
        troca = True
        tabP_atual = None


        while self.tabuleiro.encerradas < 9: #enquanto o jogo grande não acabar, continua
            # Cada rodada é uma iteração do loop
            # print(f"Encerradas: {self.tabuleiro.encerradas}")
            # clear a cada rodada
            self.jogador1.envia("clear")
            self.jogador2.envia("clear")

            jogador_atual.envia("\n\nSua vez de jogar. \n\n")
            self.outroJogador(self.jogador1, self.jogador2, jogador_atual).envia("\n\nAguarde o outro jogador jogar. \n\n")
            
            # Envia os tabueiros para os jogadores
            self.jogador1.envia(self.tabuleiro.toString())
            self.jogador2.envia(self.tabuleiro.toString())

            if troca:
                if jogador_atual == self.jogador1:
                    jogador_atual = self.jogador2
                else:
                    jogador_atual = self.jogador1
            
            # print("Rodada")
            
            if self.tabuleiro.verificarJogoEncerrou():
                break
            
            tabP_atual = self.tabuleiro.movimentoG(jogador_atual, tabP_atual)
            

        #return self.tabuleiro.fim()
        print("Fim do jogo")
        fim = self.tabuleiro.fim(self.jogador1, self.jogador2)

        if fim == 0:
            self.enviarVencedor(self.jogador1)
        elif fim == 1:
            self.enviarVencedor(self.jogador2)
        else:
            self.enviarEmpate()
        
    
    def close(self):
        self.canal.close()
        self.terminate()
        self.join()


    def run(self):
        self.start()
        self.canal.close()


export = Jogo