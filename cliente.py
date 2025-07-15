import socket

HOST = '192.168.0.105'  # IP do servidor, altere conforme sua rede
PORT = 8080

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Conectado ao servidor.\n")

        while True:
            data = s.recv(1024).decode('utf-8')
            if not data:
                print("Conexão encerrada pelo servidor.")
                break

            print(data)

            if "Sua vez" in data:
                palpite = input("Seu palpite: ")
                s.sendall(palpite.encode('utf-8'))

            if "Fim do jogo" in data or "🎉" in data:
                break

if __name__ == "__main__":
    main()
