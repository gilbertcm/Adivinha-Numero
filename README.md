# 🎯 Jogo "Adivinha o Número" — Cliente com Interface Gráfica (Tkinter)

## 🧠 Propósito do Projeto
Este projeto implementa um jogo de adivinhação de número secreto, com comunicação entre **cliente e servidor via socket TCP**.  
O cliente possui uma **interface gráfica feita com Tkinter**, onde o usuário envia palpites numéricos e recebe feedback do servidor informando se o número correto é maior, menor ou se acertou.

O jogo termina quando o número é adivinhado ou quando as tentativas se esgotam.

---

## 🚀 Como Funciona
- O **servidor** gera um número secreto aleatório.
- O **cliente** envia palpites por meio da interface gráfica.
- O **servidor** responde com dicas: `"maior"`, `"menor"` ou `"acertou"`.
- A **interface** exibe o resultado em tempo real.
- O cliente tenta **iniciar o servidor automaticamente**, se não encontrar um.

---

## 📡 Protocolo de Transporte
O protocolo utilizado é o **TCP (Transmission Control Protocol)**, garantindo:
- Confiabilidade na entrega das mensagens
- Ordem correta dos dados
- Sem perdas, ideal para manter a integridade do estado do jogo

---

## 📁 Estrutura do Projeto


---

## 💻 Como Executar

### 1. Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
''

### Verificar/Definir IP e Porta

HOST = 'SEU_ENDEREÇO_IP'
PORT = 8080
## 🔄 Protocolo de Comunicação

### 🔗 Fases de Comunicação

#### ✅ Conexão:
- O **cliente** tenta se conectar ao **servidor TCP**.
- Se a conexão falhar, o **servidor é iniciado automaticamente** pelo cliente.

#### 🚀 Inicialização:
- O servidor envia uma **mensagem de boas-vindas**.
- O cliente entra no modo de espera, **aguardando sua vez de jogar**.

#### 🎮 Jogadas:
- O cliente envia um palpite, por exemplo: `"42\n"`.
- O servidor responde com:
  - `"maior"` — o número secreto é **maior** que o palpite.
  - `"menor"` — o número secreto é **menor** que o palpite.
  - `"🎉 acertou"` — o jogador **acertou** o número.
  - `"😞 perdeu"` — o jogador **perdeu** o jogo.

#### 🖥 Atualização da Interface:
- O feedback do servidor é exibido visualmente no painel.
- Os campos da interface são **desabilitados** ao final da partida.

#### 🔚 Desconexão:
- A **conexão é encerrada automaticamente** após o término da partida.

---

## 🖼 Interface Gráfica (Tkinter)

- Estilo **moderno** com **modo escuro**.
- **Feedback visual com cores distintas**:
  - ✅ **Verde** para vitória (`"🎉 acertou"`)
  - ❌ **Vermelho** para derrota (`"😞 perdeu"`)
  - 🔺 **Laranja** quando o número secreto é maior
  - 🔻 **Azul** quando o número secreto é menor
- Barra de progresso animada enquanto aguarda o servidor.
- Interface **responsiva**, utilizando `after()` para manter a atualização fluida sem travar a interface gráfica.

---

## 🚀 Tecnologias Utilizadas

- Python 3.x
- Tkinter
- Sockets TCP (`socket` padrão do Python)