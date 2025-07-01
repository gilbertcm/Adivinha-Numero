import socket

def main():
    HOST = 'localhost'
    PORT = 12345

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORT))

    mensagem = cliente.recv(1024).decode()
    print(mensagem.strip())

    while True:
        entrada = input("Seu palpite: ")
        cliente.sendall(entrada.encode())

        resposta = cliente.recv(1024).decode()
        print("Servidor:", resposta.strip())

        if "ACERTOU" in resposta:
            break

    cliente.close()

if __name__ == "__main__":
    main()
