import time
import itertools
import string
import threading
from math import ceil

# Variável global para sinalizar quando a senha for encontrada
senha_encontrada_flag = threading.Event()
senha_correta_global = ""

def quebrar_senha_thread(senha_alvo, caracteres, inicio_range, fim_range, thread_id):
    """
    Função executada por cada thread para testar um subconjunto de combinações.
    """
    tamanho_senha = len(senha_alvo)
    combinacoes = itertools.product(caracteres, repeat=tamanho_senha)

    for i, tentativa_tuple in enumerate(combinacoes):
        # Pula para o intervalo designado para esta thread
        if i < inicio_range:
            continue
        if i >= fim_range:
            break

        # Se outra thread já encontrou a senha, para a execução
        if senha_encontrada_flag.is_set():
            return

        senha_tentada = "".join(tentativa_tuple)
        # print(f"[Thread {thread_id}] Tentando: {senha_tentada}") # Descomente para depuração

        if senha_tentada == senha_alvo:
            global senha_correta_global
            senha_correta_global = senha_tentada
            senha_encontrada_flag.set() # Sinaliza que a senha foi encontrada
            return

def encontrar_senha_paralelo(senha_alvo, caracteres, num_threads):
    """
    Coordena a quebra de senha usando múltiplas threads.
    """
    print(f"--- Início da Execução Paralela com {num_threads} Threads ---")
    inicio_total = time.time()

    tamanho_senha = len(senha_alvo)
    espaco_busca_total = len(caracteres) ** tamanho_senha
    print(f"Espaço de busca total: {espaco_busca_total} combinações")

    # Divide o trabalho entre as threads
    trabalho_por_thread = ceil(espaco_busca_total / num_threads)
    threads = []

    for i in range(num_threads):
        inicio_range = i * trabalho_por_thread
        fim_range = min((i + 1) * trabalho_por_thread, espaco_busca_total)
        
        thread = threading.Thread(
            target=quebrar_senha_thread,
            args=(senha_alvo, caracteres, inicio_range, fim_range, i + 1)
        )
        threads.append(thread)
        thread.start()
        print(f"Thread {i+1} iniciada para o intervalo [{inicio_range}, {fim_range-1}]")

    # Espera todas as threads terminarem ou a senha ser encontrada
    for thread in threads:
        thread.join()

    fim_total = time.time()

    if senha_encontrada_flag.is_set():
        print(f"\nSenha encontrada: {senha_correta_global}")
    else:
        print("\nSenha não encontrada.")

    print(f"Tempo de execução total: {fim_total - inicio_total:.4f} segundos")
    print("--- Fim da Execução Paralela ---")

if __name__ == "__main__":
    # --- Configuração ---
    CARACTERES_POSSIVEIS = string.digits
    CARACTERES_POSSIVEIS += string.ascii_lowercase 

    SENHA_ALVO = "987asd"
    NUMERO_DE_THREADS = 4 # Ajuste conforme o número de núcleos do seu processador

    print(f"Iniciando quebra de senha para '{SENHA_ALVO}' com {NUMERO_DE_THREADS} threads...")
    encontrar_senha_paralelo(SENHA_ALVO, CARACTERES_POSSIVEIS, NUMERO_DE_THREADS)