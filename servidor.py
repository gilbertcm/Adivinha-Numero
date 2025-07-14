import socket
import threading
import random

jogadores = []
lock = threading.Lock()
numero_secreto = random.randint(1, 100)
tentativas = {}


def broadcast(msg):
    for jogador in jogadores:
        jogador.sendall(msg.encode())

def handle_client(conn, jogador_id):
    global numero_secreto
    conn.sendall("BEMVINDO\n".encode())

    with lock:
        if len(jogadores) < 2:
            conn.sendall("AGUARDE_JOGADOR\n".encode())

    while len(jogadores) < 2:
        pass  # espera o segundo jogador conectar

    broadcast(f"JOGADOR_{jogador_id + 1}_CONECTADO\n")

    tentativas[jogador_id] = 0

    while True:
        if jogadores.index(conn) == handle_client.vez:
            conn.sendall("SUA_VEZ\n".encode())
            dados = conn.recv(1024).decode().strip()

            if dados.startswith("PALPITE:"):
                palpite = int(dados.split(":")[1])
                tentativas[jogador_id] += 1

                if palpite < numero_secreto:
                    conn.sendall("RESPOSTA:MAIOR\n".encode())
                elif palpite > numero_secreto:
                    conn.sendall("RESPOSTA:MENOR\n".encode())
                else:
                    broadcast(f"RESPOSTA:ACERTOU:{tentativas[jogador_id]}\n")
                    broadcast(f"FIM:JOGADOR_{jogador_id + 1}_VENCEU\n")
                    break

                handle_client.vez = 1 - handle_client.vez  # alterna jogador
        else:
            conn.sendall("AGUARDE_VEZ\n".encode())

    conn.close()


def main():
    HOST = '0.0.0.0'
    PORT = 12345
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen(2)
    print(f"[SERVIDOR] Aguardando conexões em {HOST}:{PORT}...")

    handle_client.vez = 0

    while len(jogadores) < 2:
        conn, addr = servidor.accept()
        print(f"[+] Jogador {len(jogadores)+1} conectado: {addr}")
        jogadores.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, len(jogadores)-1))
        thread.start()

if __name__ == "__main__":
    main()
