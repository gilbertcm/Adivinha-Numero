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

    def add_player(self, conn, addr):
        player_id = len(self.jogadores)
        self.jogadores.append({'conn': conn, 'addr': addr})
        return player_id

    def handle_client(self, player_id):
        conn = self.jogadores[player_id]['conn']
        conn.sendall("Bem-vindo ao jogo de Adivinhação!\n".encode('utf-8'))

        while not self.venceu:
            with self.lock:
                if len(self.jogadores) < 2:
                    conn.sendall("Aguardando o segundo jogador se conectar...\n".encode('utf-8'))
                    time.sleep(1)
                    continue

                if self.vez != player_id:
                    conn.sendall("Aguarde sua vez...\n".encode('utf-8'))
                    time.sleep(1)
                    continue

                conn.sendall("Sua vez! Digite um número entre 1 e 100: ".encode('utf-8'))
                try:
                    data = conn.recv(1024).decode('utf-8')
                    if not data:
                        break
                    palpite = int(data.strip())
                except:
                    conn.sendall("Entrada inválida. Tente novamente.\n".encode('utf-8'))
                    continue

                self.tentativas[player_id] += 1

                if palpite < self.numero_secreto:
                    conn.sendall("O número é maior!\n".encode('utf-8'))
                elif palpite > self.numero_secreto:
                    conn.sendall("O número é menor!\n".encode('utf-8'))
                else:
                    self.venceu = True
                    self.mostrar_resultado(player_id)
                    break

                self.vez = 1 - player_id  # troca a vez

        conn.close()

    def mostrar_resultado(self, vencedor_id):
        for i, jogador in enumerate(self.jogadores):
            msg = f"\n🎉 Fim do jogo! Jogador {vencedor_id + 1} acertou com {self.tentativas[vencedor_id]} tentativas!\n"
            msg += f"Jogador {i + 1} fez {self.tentativas[i]} tentativas.\n"
            jogador['conn'].sendall(msg.encode('utf-8'))

def main():
    HOST = '0.0.0.0'
    PORT = 8080

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)
    print("Servidor de Adivinhação iniciado na porta 8080.\nAguardando jogadores...")

    game = Game()

    while len(game.jogadores) < 2:
        conn, addr = server.accept()
        player_id = game.add_player(conn, addr)
        threading.Thread(target=game.handle_client, args=(player_id,)).start()
        print(f"Jogador {player_id + 1} conectado de {addr}")

if __name__ == "__main__":
    main()
