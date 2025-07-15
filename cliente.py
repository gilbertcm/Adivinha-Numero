import socket
import time

def descobrir_servidor(timeout=10):
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp.bind(('', 54545))
    udp.settimeout(timeout)

    print("Procurando servidor...")
    try:
        msg, addr = udp.recvfrom(1024)
        if msg.startswith(b'SERVIDOR_JOGO:'):
            porta = int(msg.decode().split(':')[1])
            print(f"Servidor encontrado em {addr[0]}:{porta}")
            return addr[0], porta
    except socket.timeout:
        print("Tempo esgotado. Servidor não encontrado.")
    finally:
        udp.close()

    return None, None

def main():
    HOST, PORT = descobrir_servidor()
    if not HOST:
        print("Não foi possível encontrar o servidor.")
        return

    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((HOST, PORT))
    except Exception as e:
        print(f"Erro ao conectar ao servidor: {e}")
        return

    try:
        while True:
            msg = cliente.recv(1024).decode().strip()
            if not msg:
                break
            print(f"[Servidor] {msg}")

            if msg == "SUA_VEZ":
                palpite = input("Seu palpite: ")
                cliente.sendall(f"PALPITE:{palpite}\n".encode())

            elif msg.startswith("FIM:"):
                print("Fim de jogo.")
                break
    except KeyboardInterrupt:
        print("Conexão encerrada pelo usuário.")
    finally:
        cliente.close()

if __name__ == "__main__":
    main()
