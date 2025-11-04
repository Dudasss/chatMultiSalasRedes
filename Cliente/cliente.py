import socket
import threading

# Flag para controlar a execução das threads
rodando = True


def receive_messages(client_socket):
    """
    Recebe mensagens enviadas pelo servidor enquanto a conexão estiver ativa.

    A função:
    1. Mantém um loop contínuo enquanto a variável global 'rodando' for True.
    2. Aguarda mensagens vindas do servidor através do socket do cliente.
    3. Exibe as mensagens recebidas no console.
    4. Caso a conexão seja encerrada ou ocorra falha na recepção,
       interrompe o loop e finaliza a execução.
    5. Em caso de erro inesperado, exibe a causa e encerra a conexão de forma segura.
    """
    global rodando
    while rodando:
        try:
            mensagem = client_socket.recv(1024).decode('utf-8')
            if mensagem:
                print(mensagem)
            else:
                print("Conexão falhou.")
                rodando = False
                break
        except Exception as e:
            if rodando:
                print("Erro ao receber mensagens. Desconectando.")
            rodando = False
            print(f"Saindo...")
            # print(f"Erro: {e}")
            break


def send_messages(client_socket):
    """
    Envia mensagens do cliente para o servidor enquanto a conexão estiver ativa.

    A função:
    1. Mantém um loop contínuo enquanto a variável global 'rodando' for True.
    2. Lê mensagens digitadas pelo usuário no terminal.
    3. Envia as mensagens codificadas em UTF-8 para o servidor.
    4. Caso o usuário digite '/exit' ou '/quit', encerra a comunicação e o loop.
    5. Trata interrupções do teclado (Ctrl+C ou Ctrl+D), enviando o comando de saída
       e encerrando a conexão de forma segura.
    """
    global rodando
    while rodando:
        try:
            mensagem = input()
            if mensagem:
                client_socket.send(mensagem.encode('utf-8'))
                if mensagem.lower() == '/exit' or mensagem.lower() == '/quit':
                    client_socket.send('/exit'.encode('utf-8'))
                    rodando = False
                    break
        except (EOFError, KeyboardInterrupt):
            print("Desconectando...")
            client_socket.send('/exit'.encode('utf-8'))
            rodando = False
            break


def main():
    """
        Função principal que inicializa o cliente do chat,
        estabelece a conexão com o servidor e gerencia as threads de envio e recebimento de mensagens.

        A função:
        1. Define o endereço IP e a porta do servidor (pode ser configurado manualmente).
        2. Cria um socket TCP (AF_INET para IPv4 e SOCK_STREAM para TCP).
        3. Estabelece a conexão com o servidor e exibe mensagem de confirmação.
        4. Solicita o nome do usuário e o envia ao servidor para identificação.
        5. Exibe os comandos disponíveis no chat.
        6. Cria e inicia duas threads:
           - Uma para envio de mensagens (`send_messages`)
           - Outra para recebimento de mensagens (`receive_messages`)
        7. Aguarda o término das threads antes de encerrar a conexão.
        8. Fecha o socket e encerra a execução do cliente de forma segura.
    """
    # Solicitar o ip host e a porta
    # server_host = input("Digite o enderço de IP do Servidor: ")
    # server_port = int(input("Digite a porta do servidor: "))
    server_host = '127.0.0.1'
    server_port = 7856
    # CRIANDO O SCOKET, AF_INET -> ipv4, SOCK_STREAM -> TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # connect() estabalece a conexão com servidor
        client_socket.connect((server_host, server_port))
        print(f"Conectado ao servidor em  {server_host}:{server_port}")
    except Exception as e:
        print(f"Erro: {e}")
        return
    # O nome visivel do cliente ao trocar mensagens
    nome = input("Digite seu nome: ")
    client_socket.send(nome.encode('utf-8'))

    print("\n--- Conectado ao Chat! ---")
    print("Comandos disponíveis: /join #sala, /leave, /exit, /private <nome_destinatario> <sua mensagem>")

    # inciando as threads de envio e recebimento
    thread_enviar = threading.Thread(target=send_messages, args=(client_socket, ))
    thread_receber = threading.Thread(target=receive_messages, args=(client_socket,))
    thread_enviar.start()
    thread_receber.start()

    # aguardar threads finalizarem
    thread_enviar.join()
    thread_receber.join()

    print("Desconectado.")
    client_socket.close()  # encerrando a conexão do cliente


if __name__ == "__main__":
    main()
