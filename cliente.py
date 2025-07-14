import socket

def main():
    HOST = input("Digite o IP do servidor: ")  
    PORT = 12345

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORT))

    while True:
        msg = cliente.recv(1024).decode().strip()
        print(f"[Servidor] {msg}")

        if msg == "SUA_VEZ":
            palpite = input("Seu palpite: ")
            cliente.sendall(f"PALPITE:{palpite}\n".encode())

        elif msg.startswith("FIM:"):
            break

    cliente.close()

if __name__ == "__main__":
    main()
