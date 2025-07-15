import socket
import threading
import random
import time

class Game:
    def __init__(self):
        self.lock = threading.Lock()
        self.numero_secreto = random.randint(1, 100)
        self.jogadores = []
        self.tentativas = [0, 0]
        self.vez = 0
        self.venceu = False
        self.turn_event = threading.Event()
        self.turn_event.set()  # Vez do jogador 0 começa liberada
        self.wait_msg_sent = [False, False]

    def add_player(self, conn, addr):
        player_id = len(self.jogadores)
        self.jogadores.append({'conn': conn, 'addr': addr})
        return player_id

    def handle_client(self, player_id):
        conn = self.jogadores[player_id]['conn']
        conn.sendall("Bem-vindo ao jogo de Adivinhação!\n".encode('utf-8'))

        while not self.venceu:
            if self.vez != player_id:
                # Espera o evento da vez do jogador
                self.turn_event.wait()

                # Envia mensagem de aguarde apenas uma vez
                if not self.wait_msg_sent[player_id]:
                    try:
                        conn.sendall("Aguarde sua vez...\n".encode('utf-8'))
                    except:
                        break
                    self.wait_msg_sent[player_id] = True
                # Pequena pausa para não travar a CPU
                time.sleep(0.05)
                continue
            else:
                self.wait_msg_sent[player_id] = False
                try:
                    conn.sendall("Sua vez! Digite um número entre 1 e 100: ".encode('utf-8'))
                    data = conn.recv(1024).decode('utf-8').strip()
                    if not data:
                        break
                    palpite = int(data)
                except:
                    try:
                        conn.sendall("Entrada inválida. Tente novamente.\n".encode('utf-8'))
                    except:
                        break
                    continue

                with self.lock:
                    self.tentativas[player_id] += 1
                    if palpite < self.numero_secreto:
                        conn.sendall("O número é maior!\n".encode('utf-8'))
                    elif palpite > self.numero_secreto:
                        conn.sendall("O número é menor!\n".encode('utf-8'))
                    else:
                        self.venceu = True
                        self.mostrar_resultado(player_id)
                        break

                    # Troca a vez
                    self.vez = 1 - player_id
                    self.turn_event.clear()
                    self.turn_event.set()

        conn.close()

    def mostrar_resultado(self, vencedor_id):
        msg = (f"\n🎉 Fim do jogo! Jogador {vencedor_id + 1} acertou com "
               f"{self.tentativas[vencedor_id]} tentativas!\n")
        for i, jogador in enumerate(self.jogadores):
            try:
                jogador['conn'].sendall(msg.encode('utf-8'))
                stats = f"Jogador {i + 1} fez {self.tentativas[i]} tentativas.\n"
                jogador['conn'].sendall(stats.encode('utf-8'))
            except:
                pass

def main():
    HOST = '0.0.0.0'
    PORT = 8080

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)
    print("Servidor iniciado na porta 8080. Aguardando jogadores...")

    game = Game()

    while len(game.jogadores) < 2:
        conn, addr = server.accept()
        player_id = game.add_player(conn, addr)
        threading.Thread(target=game.handle_client, args=(player_id,), daemon=True).start()
        print(f"Jogador {player_id + 1} conectado de {addr}")

    # Mantém o servidor rodando
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
