import socket
import threading
import random

def handle_client(conn, addr):
    print(f"[+] Conectado por {addr}")
    numero_secreto = random.randint(1, 100)
    tentativas = 0

    conn.sendall("Bem-vindo ao jogo! Adivinhe um número entre 1 e 100:\n".encode())
    
    while True:
        tentativa = conn.recv(1024).decode().strip()
        tentativas += 1
        if not tentativa.isdigit():
            conn.sendall("Digite um número valido!\n".encode())
            continue

        chute = int(tentativa)

        if chute < numero_secreto:
            conn.sendall(b"MAIOR\n")
        elif chute > numero_secreto:
            conn.sendall(b"MENOR\n")
        else:
            conn.sendall(f"ACERTOU! Tentativas: {tentativas}\n".encode())
            break

    conn.close()
    print(f"[-] Conexao encerrada com {addr}")

def main():
    HOST = 'localhost'
    PORT = 12345

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen()

    print(f"[SERVIDOR] Aguardando conexões em {HOST}:{PORT}...")

    while True:
        conn, addr = servidor.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()