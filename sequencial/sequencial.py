import time
import itertools
import string

def encontrar_senha(senha_correta, caracteres):
    """
    Tenta encontrar a senha testando todas as combinações possíveis de forma sequencial.

    Argumentos:
        senha_correta (str): A senha que estamos tentando adivinhar.
        caracteres (str): O conjunto de caracteres a ser usado na geração de senhas.
    """
    print("--- Início da Execução Sequencial ---")
    inicio = time.time()
    tamanho_senha = len(senha_correta)

    # Gera todas as combinações possíveis para o tamanho da senha
    combinacoes = itertools.product(caracteres, repeat=tamanho_senha)

    tentativas = 0
    for tentativa in combinacoes:
        tentativas += 1
        senha_tentada = "".join(tentativa)
        # print(f"Tentando: {senha_tentada}") # Descomente para ver o progresso
        if senha_tentada == senha_correta:
            fim = time.time()
            print(f"\nSenha encontrada: {senha_tentada}")
            print(f"Tempo de execução: {fim - inicio:.4f} segundos")
            print(f"Total de tentativas: {tentativas}")
            print("--- Fim da Execução Sequencial ---")
            return senha_tentada

    fim = time.time()
    print(f"\nSenha não encontrada no conjunto de caracteres fornecido.")
    print(f"Tempo de execução: {fim - inicio:.4f} segundos")
    print("--- Fim da Execução Sequencial ---")
    return None

if __name__ == "__main__":
    # --- Configuração ---
    # Para senhas numéricas, use string.digits
    # Para senhas alfanuméricas (minúsculas), use string.ascii_lowercase
    # Para senhas mais complexas, combine os conjuntos
    CARACTERES_POSSIVEIS = string.digits
    #CARACTERES_POSSIVEIS += string.ascii_lowercase 

    SENHA_ALVO = "123abc"

    # --- Origem da Solução ---
    # Este código sequencial foi desenvolvido com base em princípios fundamentais de
    # algoritmos de força bruta e com o auxílio da IA Gemini do Google para
    # otimizar a geração de combinações com a biblioteca `itertools`.
    # A lógica principal é um loop que testa cada possibilidade gerada.
    print(f"Origem da solução sequencial: Desenvolvido com auxílio da IA Gemini (Google).")
    print(f"Iniciando quebra de senha para '{SENHA_ALVO}'...")

    encontrar_senha(SENHA_ALVO, CARACTERES_POSSIVEIS)