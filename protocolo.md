# Protocolo da Camada de Aplicação - Jogo "Adivinha o Número"

## Estados do Jogo

- `ESPERANDO_CONEXAO`: O servidor aguarda conexões TCP dos clientes.
- `JOGANDO`: Cliente conectado tenta adivinhar o número.
- `FIM`: O cliente acertou o número e a conexão é encerrada.

## Mensagens do Cliente

- Envia uma string com o palpite (ex: `"42"`).

## Mensagens do Servidor

- `MAIOR`: O número secreto é maior que o palpite.
- `MENOR`: O número secreto é menor que o palpite.
- `ACERTOU! Tentativas: N`: O número foi descoberto, e N indica o número de tentativas.

## Observações

- Cada cliente possui uma sessão de jogo independente.
- A comunicação ocorre por meio de strings em UTF-8, separadas por `\n`.
