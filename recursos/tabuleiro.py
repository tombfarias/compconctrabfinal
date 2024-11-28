from jogadores import Jogador
def conv(tab, coord, jogador):
    coords = [0,1,2]
    while True:
        try:
            vert, hori = int(coord[0])-1, int(coord[-1])-1
            print("try")
            if vert in coords and hori in coords:
                break
            else:
                jogador.envia("Erro: As coordenadas devem estar entre 1,2,3")
                coord = jogador.recebe(1024)
        except ValueError:
            #print("except")
            jogador.envia("Erro: Coordenadas inválidas, tente novamente")
            coord = jogador.recebe(1024)
    if tab == 'P':
        return vert, hori
    if tab == 'G':
        r = 0
        for i in range(vert):
            r += 3
        r += hori
        return r
        

class tab_P:
    def __init__(self):
        self.matrizP = [[0 for i in range(3)] for j in range(3)]
        self.placar1 = [0,0,0,0,0,0,0,0,0]
        self.placar2 = [0,0,0,0,0,0,0,0,0]
        self.ocupadas = 0
        self.vitoria = 0

    def movimento(self,player, vert, hori): 
        if self.matrizP[vert][hori] != 0 or (vert > 3) or (hori > 3):
            player.envia("Erro: Movimento inválido")
            return 0 #se a casa já estiver ocupada ou nao existir
        else:
            self.matrizP[vert][hori] = player
            pos = conv('G', str(vert)+str(hori))
            self.placar1[pos] = 1
            self.placar2[pos] = player 
            print(self.placar1)
            print(self.placar2)
            if self.fim(vert, hori,player): #testa se o tabuleiro acabou
                self.vitoria = player #se acabou define vitória
                print(f'{self.vitoria} venceu esse tabuleiro')
            if self.ocupadas == 9: #se ocupou todas as casas e ainda não tem vitória, deu velha
                self.vitoria = 'V'
                print("Deu velha nesse tabuleiro")
            return 1 #Se alguma jogada foi feita
    
    def fim(self, v,h, player):
        #lista_A, lista_B = [],[]
        print("V= ",v)
        print("H=",h)
        r = False
        if ((v+h) == 4 or v==h):
            if self.matrizP[0][0] == self.matrizP[1][1] == self.matrizP[2][2] == player:
                print("vitoria da diagonal prnicipal")
                r = True
            if self.matrizP[2][0] == self.matrizP[1][1] == self.matrizP[0][2] == player:
                print("vitoria da diagonal secundaria")
                r = True
        
        
        if self.matrizP[v][0] == self.matrizP[v][1] == self.matrizP[v][2] == player:
            #print("vitoria da linha")
            r = True
        
        if self.matrizP[0][h] == self.matrizP[1][h] == self.matrizP[2][h] == player:
            #print("vitoria da coluna")
            r = True
        
        return r
    
        
    def print(self):
        for linha in self.matrizP:
            print(linha)


class tab_G:
    def __init__(self):
        self.matrizG = [tab_P() for i in range(9)]
        self.placar1 = [0,0,0,0,0,0,0,0,0]
        self.placar2 = [0,0,0,0,0,0,0,0,0]
        self.encerradas = 0
        self.vitoria = 0
    
    def movimentoG(self, coord, player):
        if self.matrizG[coord].vitoria != 0: #Vitoria começa com 0, 1 se deu velha X ou O se alguém já venceu
            self.placar1[coord] = 1
            self.placar2[coord] = self.matrizG[coord].vitoria
            self.encerradas = sum(self.placar1)
            print(f"Tabuleiro encerrado, aqqui venceu {self.matrizG[coord].vitoria}")
            return 10
        
        B = input(f'Jogada tab menor {coord + 1} \n player = {player} \n')
        if B.upper() == "FIM":
            print("Digite 'fim' novamente")
            return 10
        B1, B2 = conv('P', B)
        print(B1,B2)
        jogada = self.matrizG[coord].movimento(player, B1,B2) 
        if jogada == 0: #Movimento inválido dentro do tab_pequeno
            return 11
        else:
            r = conv('G', B)
            print("Jogador enviado para tab", r + 1)
            return r
        

    def toString(self):
        mensagem = ''
        for LINHA in range(3):
            for linha in range(3):
                for matriz in range(3*LINHA,3*(LINHA+1)):
                    mensagem = mensagem + "| " + str(self.matrizG[matriz].matrizP[linha]) + " |"
                mensagem = mensagem + '\n' 
            mensagem = mensagem + "----------------------------------------\n"
        return str(mensagem)
            
    def fim(self, j1,j2):
        pontosA = 0
        pontosB = 0
        pontosV = 0
        for player in self.placar2:
            if player == 'X':
                pontosA+=1
            elif player == 'O':
                pontosB+=1
            else:
                pontosV+=1
        if pontosA>pontosB:
            self.vitoria = "X"
            j1.envia("Você venceu!")
        elif pontosB>pontosA:
            self.vitoria = "O"
            j2.envia("Você venceu!")
        else:
            self.vitoria = "Velha"
            j1.envia("Empate!")
            j2.envia("Empate!")
            return 0;
        print(f"{self.vitoria} venceu o jogo")
        return 1;


export = tab_G, tab_P, conv