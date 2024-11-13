def conv(tab, coord):
    vert, hori = int(coord[0]), int(coord[-1])
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
        self.ocupadas = 0
        self.vitoria = 0

    def movimento(self,player, vert, hori): 
        if self.matrizP[vert][hori] != 0:
            print("Movimento inválido")
            return 0 #se a casa já estiver ocupada
        else:
            self.matrizP[vert][hori] = player
            self.ocupadas+=1 #se não estiver ocupada
            if self.fim(): #testa se o tabuleiro acabou
                self.vitoria = player #se acabou define vitória
                print(f'{self.vitoria} venceu esse tabuleiro')
            if self.ocupadas == 9: #se ocupou todas as casas e ainda não tem vitória, deu velha
                self.vitoria = 1
                print("Deu velha nesse tabuleiro")
            return 1 #Se alguma jogada foi feita
    
    def fim(self):
        if self.ocupadas >= 3:
            for i in range(3):
                if ((self.matrizP[i][0] == self.matrizP[i][1] and self.matrizP[i][1] == self.matrizP[i][2]) or 
                    (self.matrizP[0][i] == self.matrizP[1][i] and self.matrizP[1][i] == self.matrizP[2][i])):
                    return True
                if((self.matrizP[0][0] == self.matrizP[1][1] and self.matrizP[1][1] == self.matrizP[2][2]) or
                   (self.matrizP[2][0] == self.matrizP[1][1] and self.matrizP[1][1] == self.matrizP[0][2])):
                    return True
        return False
        
    def print(self):
        for linha in self.matrizP:
            print(linha)


class tab_G:
    def __init__(self):
        self.matrizG = [tab_P() for i in range(9)]
        self.encerradas = 0
        self.vitoria = 0
    
    def movimentoG(self, coord, player):
        if self.matrizG[coord].vitoria != 0: #Vitoria começa com 0, 1 se deu velha X ou O se alguém já venceu
            print("Tabuleiro encerrado")
            return 10
        
        B = input("Jogada tab menor \n")
        B1, B2 = conv('P', B)#provisório
        print(B1,B2)
        #tratar o B pra ser entrada
        jogada = self.matrizG[coord].movimento(player, B1,B2) 
        if jogada == 0: #Movimento inválido dentro do tab_pequeno
            return 11
        else:
            r = conv('G', B)
            print("Jogador enviado para tab", r)
            return r
        

    def print(self):
        for LINHA in range(3):
            for linha in range(3):
                for matriz in range(3*LINHA,3*(LINHA+1)):
                    print("|", (self.matrizG[matriz]).matrizP[linha],"|", end='')
                print('\n')
            print("----------------------------------------")


export = tab_G, tab_P, conv