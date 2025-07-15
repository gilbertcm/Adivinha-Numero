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
        self.barreira = threading.Barrier(2)
        self.wait_msg_sent = [False, False]

    def add_player(self, conn, addr):
        player_id = len(self.jogadores)
        self.jogadores.append({'conn': conn, 'addr': addr})
        return player_id

    def handle_client(self, player_id):
        conn = self.jogadores[player_id]['conn']
        conn.sendall("Bem-vindo ao jogo de Adivinhação!\n".encode('utf-8'))

        # Espera ambos os jogadores entrarem
        try:
            conn.sendall("Aguardando o outro jogador entrar...\n".encode('utf-8'))
            self.barreira.wait()
            if player_id == 0:
                self.turn_event.set()
        except threading.BrokenBarrierError:
            conn.sendall("Erro ao sincronizar jogadores.\n".encode('utf-8'))
            conn.close()
            return

        while True:
            if self.venceu:
                break

            if self.vez != player_id:
                self.turn_event.wait()
                if self.venceu:
                    break
                if not self.wait_msg_sent[player_id]:
                    try:
                        conn.sendall("Aguarde sua vez...\n".encode('utf-8'))
                    except:
                        break
                    self.wait_msg_sent[player_id] = True
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
                        self.turn_event.set()  # Libera o outro jogador
                        break

                    self.vez = 1 - player_id
                    self.turn_event.clear()
                    self.turn_event.set()

        # Fecha a conexão no final
        try:
            conn.shutdown(socket.SHUT_RDWR)
        except:
            pass
        conn.close()

    def mostrar_resultado(self, vencedor_id):
        numero = self.numero_secreto
        for i, jogador in enumerate(self.jogadores):
            try:
                if i == vencedor_id:
                    msg = (f"\n🎉 Parabéns! Você acertou o número {numero} com "
                           f"{self.tentativas[i]} tentativa(s)!\n")
                else:
                    msg = (f"\n😞 Você errou. O número era {numero}. "
                           f"O jogador {vencedor_id + 1} venceu com {self.tentativas[vencedor_id]} tentativa(s).\n")

                jogador['conn'].sendall(msg.encode('utf-8'))

                resumo = f"Resumo: Jogador {i + 1} fez {self.tentativas[i]} tentativa(s).\n"
                jogador['conn'].sendall(resumo.encode('utf-8'))
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

    # Mantém o servidor ativo
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
