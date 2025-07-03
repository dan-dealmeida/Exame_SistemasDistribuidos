import socket
import itertools
import time
import threading

def cliente():
    """
    Cliente que se conecta ao servidor, recebe uma tarefa e tenta quebrar a senha.
    """
    HOST = '127.0.0.1'  # O endereço do servidor
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("--- Cliente de Quebra de Senhas ---")
        try:
            s.connect((HOST, PORT))
            print("Conectado ao servidor. Aguardando tarefa...")
        except ConnectionRefusedError:
            print("Não foi possível conectar ao servidor. Verifique se o servidor está online.")
            return

        # Recebe a tarefa do servidor
        data = s.recv(1024).decode('utf-8')
        if not data:
            return
            
        senha_alvo, caracteres, tamanho_senha, inicio_range, fim_range = data.split(';')
        tamanho_senha = int(tamanho_senha)
        inicio_range = int(inicio_range)
        fim_range = int(fim_range)

        print(f"Tarefa recebida: Quebrar senha de {tamanho_senha} dígitos no intervalo [{inicio_range}, {fim_range-1}]")
        
        # Gera as combinações para o seu intervalo
        combinacoes = itertools.product(caracteres, repeat=tamanho_senha)
        
        # Thread para escutar mensagens de parada do servidor
        parar_flag = threading.Event()
        def escutar_servidor(sock, flag):
            try:
                msg = sock.recv(1024)
                if msg == b'PARAR':
                    flag.set()
            except:
                pass

  
        listener = threading.Thread(target=escutar_servidor, args=(s, parar_flag))
        listener.daemon = True
        listener.start()

        tempo_inicial = time.time()

        for i, tentativa_tuple in enumerate(combinacoes):
            if i < inicio_range:
                continue
            if i >= fim_range:
                break

            if parar_flag.is_set():
                print("Recebido sinal de parada do servidor. Encerrando.")
                return

            senha_tentada = "".join(tentativa_tuple)
            if senha_tentada == senha_alvo:
                tempo_final = time.time()
                tempo_execucao = tempo_final - tempo_inicial
                print(f"!!! Senha encontrada: {senha_tentada} !!!")
                print(f"Tempo de execução: {tempo_execucao:.4f} segundos.")
                s.sendall(f"ENCONTRADA:{senha_tentada}".encode('utf-8'))
                return # Encerra o cliente

        # Se terminar o loop e não encontrar
        print("Intervalo verificado. Senha não encontrada neste cliente.")
        s.sendall(b"NAO_ENCONTRADA")

if __name__ == "__main__":
    cliente()