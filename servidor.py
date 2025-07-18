#Integrantes: André, Breno, Ezequiel e Gilbert

import socket
import threading
import random
import time

class Game:
    """
    Gerencia o estado e a lógica de uma partida do jogo de adivinhação.
    """
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
        """
        Lida com a comunicação de um único cliente durante todo o jogo.
        Esta função é executada em uma thread separada para cada jogador.
        """
        conn = self.jogadores[player_id]['conn']
        conn.sendall("Bem-vindo ao jogo de Adivinhação!\n".encode('utf-8'))

        # Espera ambos os jogadores entrarem para iniciar o jogo
        try:
            conn.sendall("Aguardando o outro jogador entrar...\n".encode('utf-8'))
            self.barreira.wait()
            # O primeiro jogador a entrar (ID 0) é responsável por iniciar o primeiro turno
            if player_id == 0:
                self.turn_event.set()
        except threading.BrokenBarrierError:
            conn.sendall("Erro ao sincronizar jogadores.\n".encode('utf-8'))
            conn.close()
            return

        while True:
            # Se outro jogador venceu, a thread deve ser encerrada
            if self.venceu:
                break

            # Se não for a vez deste jogador, ele deve esperar
            if self.vez != player_id:
                self.turn_event.wait()
                if self.venceu:
                    break
                # Envia a mensagem de "Aguarde" apenas uma vez por turno
                if not self.wait_msg_sent[player_id]:
                    try:
                        conn.sendall("Aguarde sua vez...\n".encode('utf-8'))
                    except:
                        break 
                    self.wait_msg_sent[player_id] = True
                time.sleep(0.05)
                continue
            
            # É a vez deste jogador
            else:
                self.wait_msg_sent[player_id] = False
                try:
                    # Envia a solicitação de palpite (com '\n' no final)
                    msg_sua_vez = "Sua vez! Digite um número entre 1 e 100:\n"
                    conn.sendall(msg_sua_vez.encode('utf-8'))
                    
                    data = conn.recv(1024).decode('utf-8').strip()
                    if not data: 
                        break
                    palpite = int(data)

                except (ValueError, TypeError): 
                    try:
                        conn.sendall("Entrada inválida. Tente novamente.\n".encode('utf-8'))
                    except:
                        break
                    continue
                except Exception:
                    break


                # Lógica do jogo dentro de um lock para evitar condições de corrida
                with self.lock:
                    self.tentativas[player_id] += 1
                    if palpite < self.numero_secreto:
                        conn.sendall("O número é maior!\n".encode('utf-8'))
                    elif palpite > self.numero_secreto:
                        conn.sendall("O número é menor!\n".encode('utf-8'))
                    else: # O jogador acertou
                        self.venceu = True
                        self.mostrar_resultado(player_id)
                        self.turn_event.set() 
                        break

                    # Passa a vez para o outro jogador
                    self.vez = 1 - player_id
                    self.turn_event.clear()
                    self.turn_event.set()

        # Garante que a conexão seja fechada ao final
        print(f"Encerrando conexão com o jogador {player_id + 1}")
        conn.close()

    def mostrar_resultado(self, vencedor_id):
        """
        Envia uma mensagem final e unificada para ambos os jogadores.
        """
        numero = self.numero_secreto
        for i, jogador in enumerate(self.jogadores):
            try:
                if i == vencedor_id:
                    msg = (f"\n🎉 Parabéns! Você acertou o número {numero} com "
                           f"{self.tentativas[i]} tentativa(s)!\n")
                else:
                    msg = (f"\n😞 Você perdeu. O número era {numero}.\n"
                           f"O jogador {vencedor_id + 1} venceu com {self.tentativas[vencedor_id]} tentativa(s).\n"
                           f"Você fez {self.tentativas[i]} tentativa(s).\n")

                # Envia a mensagem de resultado única
                jogador['conn'].sendall(msg.encode('utf-8'))
            except:
                # Ignora erros caso o cliente já tenha desconectado
                pass

def main():
    HOST = '0.0.0.0' 
    PORT = 8080

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    server.bind((HOST, PORT))
    server.listen(2)
    print(f"Servidor iniciado na porta {PORT}. Aguardando jogadores...")

    game = Game()

    # Aceita as 2 conexões dos jogadores
    while len(game.jogadores) < 2:
        conn, addr = server.accept()
        player_id = game.add_player(conn, addr)
        # Inicia uma thread para cada jogador
        threading.Thread(target=game.handle_client, args=(player_id,), daemon=True).start()
        print(f"Jogador {player_id + 1} conectado de {addr}")

    # Mantém a thread principal viva enquanto o jogo está acontecendo
    while not game.venceu:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print("\nServidor sendo desligado.")
            break
    
    print("Jogo terminado. O servidor será finalizado em 10 segundos.")
    time.sleep(10)
    server.close()


if __name__ == "__main__":
    main()