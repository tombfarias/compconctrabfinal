def conv(tab, coord, player):
    coords = [0,1,2]
    while True:
        try:
            vert, hori = int(coord[0])-1, int(coord[-1])-1
            #print("try")
            if vert in coords and hori in coords:
                #print("jogada aceita", vert, hori)
                break
            else: 
                player.envia("As coordenadas devem estar entre 1,2,3\n")
                coord = player.joga()
        except ValueError:
            if coord.upper() == "FIM":
                return -1,-1
            #print("except")
           # coord = player.joga() 
            player.envia("Caracteres inválidos, tente novamente\n")   
            coord = player.joga()
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
            print("Movimento inválido\n")
            player.envia("Movimento inválido\n")
            return 0 #se a casa já estiver ocupada ou nao existir
        else:
            self.matrizP[vert][hori] = player.peca
            pos = conv('G', str(vert+1)+str(hori+1), player)
            self.placar1[pos] = 1
            self.placar2[pos] = player.peca 
            #print(self.placar1)
            #print(self.placar2)
            if self.fim(vert, hori,player): #testa se o tabuleiro acabou
                self.vitoria = player #se acabou define vitória
                player.envia(f'Você venceu esse tabuleiro\n')
            if self.ocupadas == 9: #se ocupou todas as casas e ainda não tem vitória, deu velha
                self.vitoria = 'V'
                player.envia("Deu velha nesse tabuleiro\n")
            return 1 #Se alguma jogada foi feita
    
    def fim(self, v,h, player):
        #lista_A, lista_B = [],[]
        #print("V= ",v)
        #print("H=",h)
        r = False
        if ((v+h) == 4 or v==h):
            if self.matrizP[0][0] == self.matrizP[1][1] == self.matrizP[2][2] == player.peca:
                #print("vitoria da diagonal prnicipal")
                r = True
            if self.matrizP[2][0] == self.matrizP[1][1] == self.matrizP[0][2] == player.peca:
                #print("vitoria da diagonal secundaria")
                r = True
        
        
        if self.matrizP[v][0] == self.matrizP[v][1] == self.matrizP[v][2] == player.peca:
            #print("vitoria da linha")
            r = True
        
        if self.matrizP[0][h] == self.matrizP[1][h] == self.matrizP[2][h] == player.peca:
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
            palyer.envia(f"Tabuleiro encerrado, aqui venceu {self.matrizG[coord].vitoria}\n")
            return 10
        player.envia(f'Jogada tab menor {coord + 1}\n')

        B = player.joga()
        if B.upper() == "FIM":
            #print("Digite 'fim' novamente")
            return 10
        B1, B2 = conv('P', B, player)
        if B1 == -1 and B2 == -1:
            #print("Segurança")
            return 10
        #print(B1,B2)
        jogada = self.matrizG[coord].movimento(player, B1,B2) 
        if jogada == 0: #Movimento inválido dentro do tab_pequeno
            return 11
        else:
            r = conv('G', B, player)
            player.envia(f'Jogador enviado para tab {r + 1}\n')
            return r
        

    def print(self, j1, j2):
        j1msg, j2msg = "",""
        for LINHA in range(3):
            for linha in range(3):
                for matriz in range(3*LINHA,3*(LINHA+1)):
                    #print("|", (self.matrizG[matriz]).matrizP[linha],"|", end='')
                    j1msg += f"| {(self.matrizG[matriz]).matrizP[linha]} | "
                    j2msg += f"| {(self.matrizG[matriz]).matrizP[linha]} | "
                
                #print('\n')
                j1.envia(j1msg+'\n')
                j2.envia(j2msg+'\n')
                j1msg, j2msg = "",""
            print("----------------------------------------")
            j1.envia("----------------------------------------\n")
            j2.envia("----------------------------------------\n")

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
