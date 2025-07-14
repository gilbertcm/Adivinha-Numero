import socket
import time

def descobrir_servidor():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp.bind(('', 54545))
    print("Procurando servidor...")
    msg, addr = udp.recvfrom(1024)
    udp.close()

    if msg.startswith(b'SERVIDOR_JOGO:'):
        porta = int(msg.decode().split(':')[1])
        print(f"Servidor encontrado em {addr[0]}:{porta}")
        return addr[0], porta
    return None, None

def main():
    HOST, PORT = descobrir_servidor()
    if not HOST:
        print("Não foi possível encontrar o servidor.")
        return

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
