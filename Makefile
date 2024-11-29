# Rodar o server.py, server.py está na pasta server
run:
	python server/server.py

# Rodar o cliente.py, cliente.py está na pasta cliente
run-client:
	python cliente/cliente.py

test-client:
	python testeCliente.py

test-client-2:
	python testeCliente2.py

test-server:
	python testeServer.py

run-c:
	gcc -o a.out server/server.c -lm
	./a.out
	rm -f a.out