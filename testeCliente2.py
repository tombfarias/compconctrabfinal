import os
import random
import subprocess

nomes = ['José', 'Maria', 'João', 'Pedro', 'Ana', 'Carlos', 'Mariana', 'Paulo', 'Luiza', 'Rafael']
# Escolher um dos nomes da lista aleatoriamente
nome = random.choice(nomes)

nome = nome + '\n'
coordenadas = []
for i in range(500):
    coordenadas.append(str(random.randint(1, 3)) + str(random.randint(1, 3)) + '\n')
coordenadas = ''.join(coordenadas)
entrada = nome + coordenadas

# Escrever a entrada em um arquivo temporário
arquivo_entrada = 'entrada2.txt'
with open(arquivo_entrada, 'w') as f:
    f.write(entrada)

# Executar o comando make run-client e redirecionar a entrada do arquivo temporário
try:
    with open(arquivo_entrada, 'r') as f:
        subprocess.run("make run-client", stdin=f, shell=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Erro ao executar o comando: {e}")

# Remover o arquivo temporário
os.remove(arquivo_entrada)