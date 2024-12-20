from jogadores import Jogador
import time
def conv(tab, coord, jogador: Jogador):
    coords = [0,1,2]
    # print(f"coord = {coord}")
    while True:
        try:
            vert, hori = int(coord[0]), int(coord[1])
            # print("try")
            if vert in coords and hori in coords:
                break
            else:
                # print(f"vert = {vert}, hori = {hori}")
                jogador.envia("As coordenadas devem estar entre 1, 2, 3: ")
                coord = jogador.recebe(1024)
        except ValueError:
            #print("except")
            jogador.envia("Coordenadas inválidas, tente novamente: ")
            coord = jogador.recebe(1024)
    if tab == 'P':
        return vert, hori
    if tab == 'G':
        r = 0
        for i in range(vert):
            r += 3
        r += hori
        return r
        

def coordenadasParaTabP(coord):
    return coord[0] * 3 + coord[1]

class tab_P:
    def __init__(self, linha, coluna):
        self.matrizP = [[0 for i in range(3)] for j in range(3)]
        # self.placar1 = [0,0,0,0,0,0,0,0,0]
        # self.placar2 = [0,0,0,0,0,0,0,0,0]
        self.ocupadas = 0
        self.vitoria = 0
        self.linha = linha
        self.coluna = coluna
        self.terminado = False

    def getCoordenadas(self):
        return self.linha * 3 + self.coluna

    def imprimirCoordenadas(self):
        return f'({self.linha + 1}, {self.coluna + 1})'
    

    def movimento(self, player: Jogador): 
        while True:
            player.envia(f"Digite a sua jogada no tabuleiro {self.imprimirCoordenadas()}: ")
            
            coordenada = player.recebe(1024)
            # print(f"coordenada = {coordenada}")
            vert, hori = conv('P', coordenada, player)

            if self.matrizP[vert][hori] != 0 or (vert > 3) or (hori > 3):
                player.envia("Erro: Movimento inválido")
                continue
            else:
                self.matrizP[vert][hori] = player
                pos = conv('G', str(vert)+str(hori), player)
                # self.placar1[pos] = 1
                # self.placar2[pos] = player 
                self.ocupadas += 1

                ###########

                #print(self.placar1)
                #print(self.placar2)

                ############

                if self.fim(player): #testa se o tabuleiro acabou
                    self.vitoria = player #se acabou define vitória
                    self.terminado = True
                    
                if self.ocupadas == 9: #se ocupou todas as casas e ainda não tem vitória, deu velha
                    self.vitoria = 'V'
                    self.terminado = True

                return pos
    
    def fim(self, player: Jogador):
        #lista_A, lista_B = [],[]
        # print("V= ",v)
       # print("H=",h)
        r = False
       
        if self.matrizP[0][0] == self.matrizP[1][1] == self.matrizP[2][2] == player:
                # print("vitoria da diagonal prnicipal")
            r = True
        if self.matrizP[2][0] == self.matrizP[1][1] == self.matrizP[0][2] == player:
                # print("vitoria da diagonal secundaria")
            r = True
        
        for i in range(3):
            if self.matrizP[i][0] == self.matrizP[i][1] == self.matrizP[i][2] == player:
            #print("vitoria da linha")
                r = True
        
            if self.matrizP[0][i] == self.matrizP[1][i] == self.matrizP[2][i] == player:
                r = True
        
        return r
    
        
    def print(self):
        for linha in self.matrizP:
            print(linha)


class tab_G:
    def __init__(self):
        self.matrizG = []
        for i in range(3):
            for j in range(3):
                self.matrizG.append(tab_P(i, j))

        self.placar1 = [0,0,0,0,0,0,0,0,0]
        self.placar2 = [0,0,0,0,0,0,0,0,0]
        self.encerradas = 0
        self.vitoria = None
    
    def verificarJogoEncerrou(self):
        for tab in self.matrizG:
            if tab.terminado == False:
                return False
            

    def displayTabG(self):
        mensagem = ''
        mensagem = mensagem + "----------------------------------------\n"
        for i in range(3):
            for j in range(3):
                matriz = i*3 + j
                mensagem = mensagem + "| " + str(self.matrizG[matriz].vitoria) + " |"
            mensagem = mensagem + '\n'
        mensagem = mensagem + "----------------------------------------\n"
        return str(mensagem)

    def movimentoG(self, player: Jogador, tabuleiroAJogar = None):
        """
        Esse método é responsável por fazer a jogada no tabuleiro grande
        """
        
        # tabuleiro a jogar deve ser um valor inteiro de 0 a 8
        if tabuleiroAJogar == None:
            player.envia("Escolha qual tabuleiro jogar: ")
            coord = player.recebe(1024)
            coord = conv('G', coord, player)
            
        else:
            coord = tabuleiroAJogar.getCoordenadas()

        vezesNoLoop = 0
        while vezesNoLoop < 9:
            if self.matrizG[coord].terminado == True:
                    if self.verificarJogoEncerrou():
                        self.encerradas = 9
                        return None
                    player.envia("Tabuleiro já encerrado, escolha outro: ")
                    coord = player.recebe(1024)
                    coord = conv('G', coord, player)
                    vezesNoLoop += 1
                    continue
            else:
                break

        if vezesNoLoop == 9:
            self.encerradas = 9
            return None

        # jogada representa o próximo tabuleiro a ser jogado
        jogada = self.matrizG[coord].movimento(player)
        jogada = self.matrizG[jogada] 

        if jogada != None and jogada.terminado == True: #Vitoria começa com 0, 1 se deu velha X ou O se alguém já venceu
            self.placar1[coord] = 1
            self.placar2[coord] = self.matrizG[coord].vitoria
            self.encerradas = sum(self.placar1)
            
            return None
        
        time.sleep(2)

       
        return jogada
        

    def toString(self):
        mensagem = ''
        for LINHA in range(3):
            for linha in range(3):
                for matriz in range(3*LINHA,3*(LINHA+1)):
                    mensagem = mensagem + "| " + str(self.matrizG[matriz].matrizP[linha]) + " |"
                mensagem = mensagem + '\n' 
            mensagem = mensagem + "----------------------------------------\n"
        return str(mensagem)
    
    def enviarTabuleiro(self, jogador: Jogador):
        jogador.envia(self.toString())
        jogador.envia("Placar: \n")
        jogador.envia(str(self.placar1) + '\n')


            
    def fim(self, j1,j2):
        
       
        pontosEmpate = 0
        for player in self.placar2:
            if player == j1:
                j1.vitorias += 1
            elif player == j2:
                j2.vitorias += 1
            else:
                pontosEmpate += 1
        if j1.vitorias > j2.vitorias:
            self.vitoria = j1
            j1.envia("Você venceu!")
            j2.envia("Você perdeu!")
            return 0
        elif j2.vitorias > j1.vitorias:
            self.vitoria = j2
            j2.envia("Você venceu!")
            j1.envia("Você perdeu!")
            return 1
        else:
            self.vitoria = None
            j1.envia("Empate!")
            j2.envia("Empate!")
            return 2;
    


export = tab_G, tab_P, conv