# compconctrabfinal

Esse repositório contem uma implementação do super jogo da velha.
O jogo é formado por três diretórios
cliente
recursos
servidor

O diretório cliente contem o código cliente.py que deve ser executado pelo usuário:
python3 cliente2.py

O repositório recursos contem a estrutura do jogo, possuindo um código referente a criação e "cadastro" dos jogadores no jogo, um código jogo.py que possui a classe Jogo, essa classe une os outros dois elementos e é onde efetivamente o jogo está acontecendo e um código tabuleiro que constrói a estrutura do(s) tabuleiro(s) usados no jogo.

O diretório server contem o código server.py que estará sendo executado na máquina do servidor para manter o game aberto e disponível para acesso de usuários

Portanto, para funcionamento do game o server deve estar aberto para aceitação de usuários e pelo menos dois clientes devem iniciar uma conexão.

Além disso, temos no diretório server um código pyc.c, esse código em C tem como propósito mostrar a concorrência que ocorre no servidor. Possui duas threads, uma delas calcula pi usando a fórmula de Bailey repetidamente e conta quantas vezes esse valor foi calculado (como a fórmula chega ao limite do computador muito rápido, essa contagem é feita de 1000000000 em 1000000000) enquanto a outra thread estará com o servidor do jogo aberto para conexões. 
As duas threads rodam de maneira paralela, ou seja, além da concorrência do jogo, o computador do servidor ainda tem CPU disponível para fazer outras coisas, nesse caso, o cálculo de pi.

