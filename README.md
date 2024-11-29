# Trabalho Final de Computação Concorrente
Autores: André Luis Alves Martins / Tomás Barboza de Farias

## 1. Como testar
Idealmente rodando em 3 terminais diferentes, um para cada comando abaixo:
```bash
$ make run # Roda o servidor
$ make run-client # Roda o cliente
$ make test-client # Roda o conjunto de teste do cliente
$ make test-client-2 # Roda o conjunto 2 de teste do cliente
$ make test-server # Roda o conjunto de teste do servidor
```

Rodar um servidor e 2 clientes


## 2. Estrutura do projeto
O projeto foi dividido em 3 arquivos principais:
- `server.py`: Contém a implementação do servidor
- `client.py`: Contém a implementação do cliente
- `jogo.py`: Contém o processo que roda o jogo

Além disso, temos o `server.c` que roda o servidor ao mesmo tempo em que roda o algoritmo para calcular o pi

