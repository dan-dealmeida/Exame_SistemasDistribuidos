# Quebra de Senhas por Força Bruta: Sequencial, Paralelo e Distribuído

Este projeto demonstra e compara três abordagens para resolver o problema da quebra de senhas numéricas por força bruta: sequencial, paralela (com Threads) e distribuída (com Sockets).

## 🎯 Objetivo

O objetivo é analisar o desempenho, a complexidade e a escalabilidade de cada solução, destacando os ganhos obtidos com o paralelismo e a computação distribuída em um problema computacionalmente intensivo.

## 📂 Estrutura do Projeto
/
├── sequencial/       # Solução sequencial
├── paralelo/         # Solução paralela com Threads
├── distribuido/      # Solução distribuída com Sockets (servidor e cliente)
├── relatorio_e_links.txt # Análise comparativa e links
├── apresentacao.pdf  # Slides da apresentação
└── README.md         # Documentação principal

## 🚀 Como Executar

### Requisitos
- Python 3.x

### 1. Solução Sequencial

```bash
cd sequencial
python sequencial.py

### 2. Solução Paralela
```bash
cd paralelo
python paralelo.py

Você pode alterar o número de threads e a senha alvo diretamente no arquivo paralelo.py.

### 3. Solução Distribuída
Esta solução requer a execução de um servidor e um ou mais clientes.

1. Inicie o Servidor:
Abra um terminal e execute:

Bash

cd distribuido
python servidor.py
O servidor irá aguardar as conexões dos clientes. Configure o número de clientes esperados no código.

2. Inicie os Clientes:
Abra um novo terminal para cada cliente e execute:

Bash

cd distribuido
python cliente.py
Execute este comando em quantos terminais (ou máquinas na rede) você desejar. O trabalho começará assim que o número esperado de clientes se conectar ao servidor.