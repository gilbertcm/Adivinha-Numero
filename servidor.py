import socket
import threading
import random
import time

jogadores = []
lock = threading.Lock()
numero_secreto = random.randint(1, 100)
tentativas = {}

# === BROADCAST UDP PARA DESCOBERTA AUTOMÁTICA ===
def broadcast_discovery():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    msg = b'SERVIDOR_JOGO:12345'
    while True:
        try:
            udp.sendto(msg, ('<broadcast>', 54545))
            time.sleep(2)
        except Exception as e:
            print(f"[ERRO BROADCAST] {e}")
            break
    udp.close()

def broadcast(msg):
    for jogador in jogadores:
        try:
            jogador.sendall(msg.encode())
        except:
            pass

def handle_client(conn, jogador_id):
    global numero_secreto
    conn.sendall("BEMVINDO\n".encode())

    with lock:
        if len(jogadores) < 2:
            conn.sendall("AGUARDE_JOGADOR\n".encode())

    while len(jogadores) < 2:
        time.sleep(0.1)

    broadcast(f"JOGADOR_{jogador_id + 1}_CONECTADO\n")
    tentativas[jogador_id] = 0

    while True:
        try:
            if jogador_id == handle_client.vez:
                conn.sendall("SUA_VEZ\n".encode())
                dados = conn.recv(1024).decode().strip()

                if not dados:
                    break  # desconectado

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

                    handle_client.vez = 1 - handle_client.vez
            else:
                conn.sendall("AGUARDE_VEZ\n".encode())
                time.sleep(1)
        except:
            break

    conn.close()

def get_ip_local():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def main():
    HOST = '0.0.0.0'
    PORT = 12345

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORT))
    servidor.listen(2)

    ip_local = get_ip_local()
    print(f"[SERVIDOR] Rodando em {ip_local}:{PORT}")

    threading.Thread(target=broadcast_discovery, daemon=True).start()
    handle_client.vez = 0

    while len(jogadores) < 2:
        conn, addr = servidor.accept()
        print(f"[+] Jogador {len(jogadores) + 1} conectado de {addr}")
        jogadores.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, len(jogadores) - 1))
        thread.start()

if __name__ == "__main__":
    main()
