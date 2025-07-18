# 🎯 Jogo "Adivinha o Número" — Cliente com Interface Gráfica (Tkinter)

# Integrantes: André, Breno, Ezequiel e Gilbert

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

## 📡 Por que o protocolo TCP foi escolhido

- ✅ **Confiabilidade na entrega das mensagens**  
  Garante que todos os dados enviados cheguem corretamente ao destino, sem perdas.

- ✅ **Ordem correta dos dados**  
  As mensagens chegam na mesma ordem em que foram enviadas, essencial para a lógica sequencial do jogo.

- ✅ **Sem perdas de dados**  
  O TCP detecta e retransmite pacotes perdidos, garantindo a integridade da comunicação.

- ✅ **Conexão orientada (estado mantido)**  
  Permite manter o estado da conexão entre cliente e servidor, essencial para gerenciar a lógica do jogo de forma segura.

---

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
# 🎮 Jogo Adivinha o Número (Dois Jogadores)

## 🌐 Protocolo da Camada de Aplicação

Este jogo utiliza comunicação TCP entre dois jogadores, onde o servidor controla o jogo e os clientes interagem por meio de uma interface gráfica.

---

## 🎯 Eventos e Estados

### 1. 🟢 Conexão Iniciada
- **Servidor**: Aguarda conexões dos dois jogadores. Inicia o jogo assim que ambos estão conectados.
- **Cliente**: Tenta se conectar ao servidor. Caso falhe, inicia o servidor automaticamente.

---

### 2. 🚦 Inicialização do Jogo
- **Servidor**:
  - Envia mensagem de boas-vindas.
  - Informa que está aguardando o segundo jogador.
  - Sorteia um número aleatório entre 1 e 100 quando ambos estiverem conectados.
- **Cliente**:
  - Exibe mensagem de boas-vindas.
  - Aguarda a liberação da jogada.

---

### 3. 🎲 Turno de Jogada
- **Cliente (jogador da vez)**:
  - Recebe mensagem: `"Sua vez! Digite um número entre 1 e 100:"`
  - Envia o palpite ao servidor.
- **Servidor**:
  - Verifica o palpite:
    - Se correto: encerra o jogo.
    - Se incorreto: envia dica `"maior"` ou `"menor"`.

---

### 4. ⏳ Espera de Jogada
- Enquanto o outro jogador joga:
  - **Servidor → Cliente**: `"Aguarde sua vez..."`
  - **Cliente**: Desativa entrada de dados até sua vez.

---

### 5. 🏁 Fim do Jogo
- **Servidor**:
  - Informa quem venceu, quantas tentativas cada um fez e o número secreto.
- **Cliente**:
  - Exibe uma das mensagens:
    - ✅ `"🎉 Parabéns! Você acertou o número X com Y tentativas!"`
    - ❌ `"😞 Você perdeu. O número era X. O outro jogador venceu com Y tentativas."`

---

### 6. 🔌 Desconexão
- O servidor e os clientes encerram a conexão automaticamente após o fim da partida.

---

## 🔁 Mensagens Trocadas

### 🟡 Boas-vindas e Sincronização
**Servidor → Cliente:**


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