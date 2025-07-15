
import socket
import threading
import tkinter as tk
from tkinter import ttk, messagebox


HOST = '192.168.1.3'
PORT = 8080

class JogoGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("🎯 Adivinha o Número")
        self.master.geometry("400x450")
        self.master.resizable(False, False)
        self.master.configure(bg="#222")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.sock = None
        self.is_connected = False

        # --- Widgets da Interface ---
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("green.Horizontal.TProgressbar", foreground='lime', background='lime')

        self.title_label = tk.Label(master, text="Adivinha o Número", font=("Helvetica", 20, "bold"), fg="lime", bg="#222")
        self.title_label.pack(pady=20)

        self.status = tk.Label(master, text="🔌 Conectando ao servidor...", font=("Helvetica", 12), fg="white", bg="#222")
        self.status.pack(pady=5)

        self.progress = ttk.Progressbar(master, style="green.Horizontal.TProgressbar", mode="indeterminate", length=250)
        self.progress.pack(pady=10)
        self.progress.start()

        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(master, textvariable=self.input_var, font=("Helvetica", 14), width=10, justify="center", state="disabled", bg="#333", fg="white", disabledbackground="#111", insertbackground="white")
        self.input_entry.pack(pady=10)
        self.input_entry.bind("<Return>", self.enviar_palpite)

        self.enviar_btn = tk.Button(master, text="Enviar Palpite", command=self.enviar_palpite, font=("Helvetica", 12), state="disabled", bg="#444", fg="white", activebackground="#555")
        self.enviar_btn.pack()

        self.feedback = tk.Label(master, text="", font=("Helvetica", 18, "bold"), fg="white", bg="#222", height=2)
        self.feedback.pack(pady=20)

        self.info = tk.Label(master, text="", font=("Helvetica", 11), fg="#aaa", bg="#222", justify="center", wraplength=380)
        self.info.pack(side="bottom", pady=10)

        threading.Thread(target=self.conectar_ao_servidor, daemon=True).start()

    def on_closing(self):
        """Lida com o fechamento da janela."""
        if self.sock:
            self.sock.close()
        self.master.destroy()

    def conectar_ao_servidor(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((HOST, PORT))
            self.is_connected = True
            # Inicia a thread para receber mensagens
            threading.Thread(target=self.receber_mensagens, daemon=True).start()
        except Exception as e:
            self.status.config(text="❌ Falha ao conectar.")
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao servidor em {HOST}:{PORT}.\nVerifique o IP e se o servidor está rodando.\n\nDetalhes: {e}")
            self.master.after(0, self.on_closing)

    def receber_mensagens(self):
        """
        Loop para receber dados do servidor e processá-los.
        Usa um buffer para garantir que mensagens completas sejam processadas.
        """
        buffer = ""
        try:
            while self.is_connected:
                data = self.sock.recv(1024).decode("utf-8")
                if not data:
                    break
                buffer += data
                while "\n" in buffer:
                    msg, buffer = buffer.split("\n", 1)
                    if msg.strip():
                        # Usa 'after' para atualizar a GUI a partir da thread principal
                        self.master.after(0, self.tratar_mensagem, msg.strip())
        except (ConnectionAbortedError, ConnectionResetError):
            self.status.config(text="⚠️ Conexão perdida.")
        finally:
            self.is_connected = False

    def tratar_mensagem(self, msg):
        """
        Interpreta a mensagem do servidor e atualiza a interface gráfica.
        """
        # <--- MUDANÇA: Lógica de Fim de Jogo Aprimorada ---
        if "🎉" in msg or "😞" in msg:
            self.input_entry.config(state="disabled")
            self.enviar_btn.config(state="disabled")
            self.status.config(text="🏁 Jogo encerrado!", fg="white")
            self.progress.stop()
            self.progress.pack_forget()
            
            # Limpa o texto informativo para dar espaço ao resumo final
            self.info.config(text="") 

            if "🎉" in msg: # Mensagem de vitória
                self.feedback.config(text="🎉 VOCÊ VENCEU! 🎉", fg="#22DD22") # Verde Vibrante
                # Exibe os detalhes da vitória no rodapé
                self.info.config(text=msg.strip(), font=("Helvetica", 11), fg="#DDDDDD")
            
            elif "😞" in msg: # Mensagem de derrota
                self.feedback.config(text="😞 VOCÊ PERDEU 😞", fg="#FF4444") # Vermelho Vibrante
                # Exibe os detalhes da derrota no rodapé
                self.info.config(text=msg.strip(), font=("Helvetica", 11), fg="#AAAAAA")
            return

        # Mensagens durante o jogo
        if "Sua vez" in msg:
            self.status.config(text="🎯 Sua vez!", fg="lime")
            self.progress.stop()
            self.progress.pack_forget()
            self.feedback.config(text="")
            self.input_entry.config(state="normal")
            self.enviar_btn.config(state="normal")
            self.input_entry.focus()
        elif "maior" in msg.lower():
            self.feedback.config(text="🔺 O número é MAIOR", fg="#FFA500") # Laranja
        elif "menor" in msg.lower():
            self.feedback.config(text="🔻 O número é MENOR", fg="#1E90FF") # Azul
            
        # <--- MUDANÇA: Lógica para Aguardar ---
        elif "Aguarde" in msg or "Aguardando" in msg:
            self.status.config(text="⏳ " + msg, fg="#aaa")
            # Garante que a barra de progresso esteja visível e no lugar certo
            if not self.progress.winfo_ismapped():
                self.progress.pack(pady=10, after=self.status) # <-- Garante a posição correta
            self.progress.start()
            self.input_entry.config(state="disabled")
            self.enviar_btn.config(state="disabled")
            
        elif "Bem-vindo" in msg:
             self.info.config(text=msg)

    def enviar_palpite(self, event=None):
        palpite = self.input_var.get().strip()
        if palpite.isdigit():
            try:
                if self.is_connected:
                    self.sock.sendall((palpite + "\n").encode("utf-8"))
                    self.input_var.set("")
                    self.input_entry.config(state="disabled")
                    self.enviar_btn.config(state="disabled")
            except (ConnectionAbortedError, ConnectionResetError):
                self.status.config(text="Erro: Conexão perdida.")
        else:
            messagebox.showwarning("Entrada Inválida", "Por favor, digite um número válido.")


def main():
    root = tk.Tk()
    app = JogoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()