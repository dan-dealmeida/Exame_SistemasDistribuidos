import socket
import time
import string
import itertools
from math import ceil

def servidor():
    """
    Servidor que distribui o trabalho de quebra de senha para os clientes.
    """
    # --- Configuração do Servidor ---
    HOST = '127.0.0.1'  # localhost
    PORT = 65432
    NUM_CLIENTES_ESPERADOS = 2 # Defina quantos clientes irão se conectar

    # --- Configuração do Problema ---
    SENHA_ALVO = "234ads" # Senha menor para teste rápido
    CARACTERES = string.digits
    CARACTERES += string.ascii_lowercase 
    TAMANHO_SENHA = len(SENHA_ALVO)
    ESPACO_BUSCA = len(CARACTERES) ** TAMANHO_SENHA

    print("--- Servidor de Quebra de Senhas ---")
    print(f"Aguardando {NUM_CLIENTES_ESPERADOS} clientes se conectarem...")

    clientes = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(NUM_CLIENTES_ESPERADOS)

        # Aceita conexões dos clientes
        while len(clientes) < NUM_CLIENTES_ESPERADOS:
            conn, addr = s.accept()
            clientes.append(conn)
            print(f"Cliente {len(clientes)} conectado de {addr}")

        inicio_total = time.time()

        # Divide o trabalho
        trabalho_por_cliente = ceil(ESPACO_BUSCA / NUM_CLIENTES_ESPERADOS)
        
        # Envia as tarefas para cada cliente
        for i, cliente_conn in enumerate(clientes):
            inicio_range = i * trabalho_por_cliente
            fim_range = min((i + 1) * trabalho_por_cliente, ESPACO_BUSCA)
            
            # Formato da mensagem: SENHA_ALVO;CARACTERES;TAMANHO_SENHA;INICIO_RANGE;FIM_RANGE
            mensagem = f"{SENHA_ALVO};{CARACTERES};{TAMANHO_SENHA};{inicio_range};{fim_range}"
            cliente_conn.sendall(mensagem.encode('utf-8'))
            print(f"Enviando tarefa para Cliente {i+1}: range [{inicio_range}, {fim_range-1}]")

        # Aguarda o resultado dos clientes
        while True:
            for cliente_conn in clientes:
                try:
                    # Define um timeout para não bloquear indefinidamente
                    cliente_conn.settimeout(0.1)
                    data = cliente_conn.recv(1024).decode('utf-8')
                    if data:
                        if data.startswith("ENCONTRADA:"):
                            senha = data.split(":")[1]
                            fim_total = time.time()
                            print(f"\n--- SENHA ENCONTRADA PELO CLIENTE ---")
                            print(f"Senha: {senha}")
                            print(f"Tempo total de execução: {fim_total - inicio_total:.4f} segundos")
                            
                            # Avisa todos os outros clientes para pararem
                            for c in clientes:
                                c.sendall(b'PARAR')
                            
                            # Fecha conexões e encerra
                            for c in clientes:
                                c.close()
                            return
                        elif data == "NAO_ENCONTRADA":
                            print(f"Cliente {clientes.index(cliente_conn) + 1} terminou seu intervalo sem sucesso.")

                except socket.timeout:
                    continue # Continua verificando outros clientes
                except ConnectionResetError:
                    print("Um cliente desconectou.")
                    clientes.remove(cliente_conn)


if __name__ == "__main__":
    servidor()