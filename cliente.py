import socket
import threading
import tkinter as tk
from tkinter import ttk, messagebox

HOST = '192.168.1.3'  # Altere conforme sua rede
PORT = 8080

class JogoGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("🎯 Adivinha o Número")
        self.master.geometry("400x400")
        self.master.configure(bg="#222")

        self.sock = None

        # === Título
        self.title_label = tk.Label(master, text="Adivinha o Número", font=("Helvetica", 20, "bold"), fg="lime", bg="#222")
        self.title_label.pack(pady=10)

        # === Indicador de status (sua vez, aguardando etc)
        self.status = tk.Label(master, text="🔌 Conectando ao servidor...", font=("Helvetica", 12), fg="white", bg="#222")
        self.status.pack(pady=5)

        # === Animação de espera
        self.progress = ttk.Progressbar(master, mode="indeterminate", length=250)
        self.progress.pack(pady=10)
        self.progress.start()

        # === Palpite (input)
        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(master, textvariable=self.input_var, font=("Helvetica", 14), width=10, justify="center", state="disabled")
        self.input_entry.pack(pady=10)
        self.input_entry.bind("<Return>", lambda e: self.enviar_palpite())

        self.enviar_btn = tk.Button(master, text="Enviar Palpite", command=self.enviar_palpite, font=("Helvetica", 10), state="disabled")
        self.enviar_btn.pack()

        # === Resultado visual
        self.feedback = tk.Label(master, text="", font=("Helvetica", 16, "bold"), fg="white", bg="#222")
        self.feedback.pack(pady=20)

        # === Rodapé (tentativas ou fim do jogo)
        self.info = tk.Label(master, text="", font=("Helvetica", 10), fg="gray", bg="#222")
        self.info.pack(pady=10)

        threading.Thread(target=self.conectar_ao_servidor, daemon=True).start()

    def conectar_ao_servidor(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((HOST, PORT))
            self.status.config(text="✅ Conectado. Aguardando jogo começar...")
            self.receber_mensagens()
        except Exception as e:
            self.status.config(text="❌ Falha ao conectar.")
            messagebox.showerror("Erro", str(e))

    def receber_mensagens(self):
        try:
            while True:
                msg = self.sock.recv(1024).decode("utf-8").strip()
                if not msg:
                    break

                self.master.after(0, self.tratar_mensagem, msg)
        except:
            self.status.config(text="⚠️ Conexão encerrada.")

    def tratar_mensagem(self, msg):
        if "Sua vez" in msg:
            self.status.config(text="🎯 Sua vez!", fg="lime")
            self.progress.stop()
            self.feedback.config(text="")
            self.input_entry.config(state="normal")
            self.enviar_btn.config(state="normal")
            self.input_entry.focus()

        elif "maior" in msg.lower():
            self.feedback.config(text="🔺 O número é MAIOR", fg="orange")
        elif "menor" in msg.lower():
            self.feedback.config(text="🔻 O número é MENOR", fg="deepskyblue")
        elif "acertou" in msg.lower():
            self.feedback.config(text="🎉 Você acertou!", fg="lime")
        elif "Fim do jogo" in msg or "🎉" in msg:
            self.input_entry.config(state="disabled")
            self.enviar_btn.config(state="disabled")
            self.status.config(text="🏁 Jogo encerrado")
            self.progress.stop()
            self.info.config(text=msg)
        elif "Aguarde" in msg:
            self.status.config(text="⏳ Aguardando outro jogador...", fg="gray")
            self.progress.start()
            self.input_entry.config(state="disabled")
            self.enviar_btn.config(state="disabled")

    def enviar_palpite(self):
        palpite = self.input_var.get().strip()
        if palpite.isdigit() and 1 <= int(palpite) <= 100:
            try:
                self.sock.sendall(palpite.encode("utf-8"))
                self.input_var.set("")
                self.input_entry.config(state="disabled")
                self.enviar_btn.config(state="disabled")
                self.status.config(text="🔄 Aguardando resposta...", fg="gray")
            except:
                self.feedback.config(text="Erro ao enviar palpite.", fg="red")
        else:
            self.feedback.config(text="Digite um número de 1 a 100.", fg="red")

def main():
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use("clam")
    app = JogoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
