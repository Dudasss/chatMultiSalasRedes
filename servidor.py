import socket
import threading

clientes = {}  # {client_socket: nome_cliente}
salas = {}  # {nome_sala: [client_socket1, client_socket2, etc]}


def broadcast(sala, mensagem, remetente_socket):
    """
       Envia uma mensagem a todos os clientes de uma sala,
       exceto ao remetente.

       A função:
       1. Verifica se a sala existe no dicionário de salas.
       2. Percorre todos os sockets associados à sala.
       3. Envia a mensagem codificada em UTF-8 para cada cliente,
          exceto para o remetente.
       4. Caso ocorra um erro de envio, remove o cliente problemático
          da lista de salas através da função remover_cliente().
       """
    if sala in salas:
        for client_socket in salas[sala]:
            if client_socket != remetente_socket:  # se quem envia é diferente de quem recebe a mensagem será enviada
                try:
                    client_socket.send(mensagem.encode('utf-8'))
                except Exception as e:
                    print(f"Ocorreu erro: {e}")
                    remover_cliente(client_socket)  # remove o cliente com erro das salas


def remover_cliente(client_socket):
    """
    Remove o cliente de todas as estruturas de controle (lista geral e salas)
    caso ocorra um erro ou desconexão.

    A função:
    1. Obtém o nome do cliente a partir do socket.
    2. Remove-o do dicionário global de clientes.
    3. Exibe mensagem de desconexão no servidor.
    4. Percorre todas as salas e o remove de qualquer uma onde esteja presente.
    5. Notifica os demais usuários da sala sobre a saída.
    6. Encerra a conexão do cliente.
    """
    if client_socket in clientes:
        nome = clientes[client_socket]
        del clientes[client_socket]
        print(f"{nome} se desconectou.")
        for sala in salas:
            if client_socket in salas[sala]:
                salas[sala].remove(client_socket)
                broadcast(sala, f"{nome} se desconectou.", client_socket)
        client_socket.close()


def enviar_privado(remetente_nome, destinatario_nome, mensagem, remetente_socket):
    """
        Envia uma mensagem privada de um usuário para outro,
        caso o destinatário esteja conectado ao servidor.

        A função:
        1. Procura o socket do destinatário no dicionário global de clientes.
        2. Se encontrado, envia a mensagem privada codificada em UTF-8.
        3. Informa o remetente sobre o sucesso do envio.
        4. Caso ocorra erro durante o envio, exibe a falha no servidor e
           notifica o remetente.
        5. Caso o destinatário não esteja on-line, avisa o remetente de que
           o usuário não foi encontrado.
        """
    client_socket_destinatario = None
    for k, v in clientes.items():
        if v == destinatario_nome:
            client_socket_destinatario = k
            break
    mensagem_formatada = f"[Privado de {remetente_nome}: {mensagem}"

    if client_socket_destinatario:
        try:
            client_socket_destinatario.send(mensagem_formatada.encode('utf-8'))
            remetente_socket.send(f"SISTEMA: [Enviado para {destinatario_nome}]: {mensagem}".encode('utf-8'))
        except Exception as e:
            print(f"Erro: {e}\nDesconetando.")
            remetente_socket.send(f"SISTEMA: Erro ao enviar mensagem para {destinatario_nome}.".encode('utf-8'))
    else:
        remetente_socket.send(f"SISTEMA: Usuário '{destinatario_nome}' não encontrado.".encode('utf-8'))


def lidar_cliente(client_socket):
    """
        Gerencia a conexão e a comunicação inicial de um cliente com o servidor.

        A função:
        1. Recebe a primeira mensagem enviada pelo cliente, que corresponde ao seu nome de usuário.
        2. Armazena o socket e o nome no dicionário global de clientes.
        3. Exibe no console do servidor informações sobre a nova conexão.
        4. Envia ao cliente uma mensagem de boas-vindas e instruções de uso.
        5. Em caso de erro durante a conexão, exibe o erro e encerra o socket de forma segura.

        Comandos disponíveis após a conexão:
            /join #sala          → Entra em uma sala (cria se não existir)
            /leave               → Sai da sala atual
            /exit ou /quit       → Desconecta do servidor
            /private <dest> <msg> → Envia uma mensagem privada para outro usuário
    """
    try:
        # recv(): função que recebe (lê) dados enviados através de uma conexão de socket
        # 1024: a quantidade máxima de bytes que a função tentará ler de uma só vez.
        nome = client_socket.recv(1024).decode('utf-8').strip()
        clientes[client_socket] = nome
        print(f"{nome} se conectou com o endereço {client_socket.getpeername()}")
        client_socket.send("Conectado ao servidor! Use /join #nome_da_sala para entrar em uma sala. Caso ela "
                           "não exista, será criada".encode('utf-8'))
    except Exception as e:
        print(f"Erro: {e}\nDesconetando.")
        # encerra a conexão do cliente com erro
        client_socket.close()
        return

    # DEFININDO OS COMANDOS
    # /join #sala: Entra em uma sala. Se a sala não existir, o servidor a cria.
    # /leave: Sai da sala atual.
    # /exit ou /quit: Desconecta do servidor.
    # /private <nome_destinatario> <sua mensagem>: envia uma mensagem privada para outro usuário
    sala_atual = None

    while True:
        try:
            # receber/ler a mensagem do cliente
            mensagem = client_socket.recv(1024).decode('utf-8')
            if mensagem:
                if not mensagem:  # Ignora mensagens vazias
                    continue
                if mensagem.startswith('/'):
                    partes = mensagem.split(' ')
                    comando = partes[0].lower()

                    if comando == '/join':
                        if len(partes) > 1:
                            nova_sala = partes[1]
                            # sair da sala antiga, caso esteja em uma
                            if sala_atual and client_socket in salas.get(sala_atual, []):
                                salas[sala_atual].remove(client_socket)
                                broadcast(sala_atual, f"{nome} saiu da sala.", client_socket)

                            # cria sala nova, caso não exista
                            if nova_sala not in salas:
                                salas[nova_sala] = []
                                client_socket.send("Nova sala criada.".encode('utf-8'))
                                broadcast(sala_atual, "Nova sala criada.", client_socket)
                            # entrar na (nova) sala
                            salas[nova_sala].append(client_socket)
                            sala_atual = nova_sala
                            client_socket.send(f"{nome} entrou na {sala_atual}".encode('utf-8'))
                            broadcast(sala_atual, f"{nome} entrou na sala.", client_socket)
                        else:
                            client_socket.send("Uso: /join #nome_da_sala".encode('utf-8'))

                    elif comando == '/leave':
                        # sair da sala, caso esteja em uma
                        if sala_atual and client_socket in salas.get(sala_atual, []):
                            salas[sala_atual].remove(client_socket)
                            broadcast(sala_atual, f"{nome} saiu da sala", client_socket)
                            client_socket.send(f"Você saiu da sala {sala_atual}".encode('utf-8'))
                            sala_atual = None
                        else:
                            client_socket.send(f"Você não está em nenhuma sala.".encode('utf-8'))

                    elif comando == '/private':
                        if len(partes) > 2:
                            destinatario_nome = partes[1]
                            mensagem_privada = " ".join(partes[2:])
                            if destinatario_nome == nome:
                                # Impede o usuário de enviar msg para si mesmo
                                client_socket.send(
                                    "SISTEMA: Você não pode enviar uma mensagem privada para si mesmo.".encode('utf-8'))
                            else:
                                # Chama a nova função que criamos
                                enviar_privado(nome, destinatario_nome, mensagem_privada, client_socket)
                        else:
                            client_socket.send("SISTEMA: Uso: /private <nome_destinatario> <sua mensagem>"
                                               .encode('utf-8'))

                    elif comando == '/exit' or comando == '/quit':
                        break

                    else:
                        print("Comando desconhecido. Tente /join #nome_da_sala, /leave para sair da sala, /quit para "
                              "sair do servidor")
                else:
                    # Enviando mensagens normais, q ñ são comandos
                    if sala_atual:
                        texto = f"[{sala_atual}][{nome}]: {mensagem}"
                        broadcast(sala_atual, texto, client_socket)  # função que envia msg p todos os outros na sala
                    else:
                        client_socket.send(
                            "Entre em uma sala para enviar mensagens. Use /join #nome_da_sala".encode('utf-8'))
            else:
                break
        except Exception as e:
            print(f"Erro: {e}")
            print("2")
            break
    remover_cliente(client_socket)


def main():
    """
        Função principal que inicializa e executa o servidor de chat.

        A função:
        1. Define o endereço IP e a porta onde o servidor ficará ativo.
        2. Cria um socket TCP (AF_INET para IPv4 e SOCK_STREAM para TCP).
        3. Associa o socket ao endereço e porta definidos (bind).
        4. Coloca o servidor em modo de escuta, aguardando conexões de clientes.
        5. Exibe mensagem informando que o servidor está ativo.
        6. Entra em um loop contínuo que:
            - Aceita novas conexões de clientes.
            - Cria uma nova thread para cada cliente conectado,
              delegando o tratamento ao método `lidar_cliente()`.
        7. Utiliza threads em modo daemon para garantir que o servidor possa
           ser encerrado corretamente mesmo com clientes ativos.
    """
    # host = input("Digite o enderço de IP do Servidor: ")
    # port = int(input("Digite a porta do servidor: "))
    host = '127.0.0.1'
    port = 7856

    # CRIANDO O SCOKET, AF_INET -> ipv4, SOCK_STREAM -> TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))  # vinculando o socket ao ip e porta
    server_socket.listen()  # servidor em modo de escuta, para aceitar conexões

    print(f"Servidor escutando em {host}:{port}")
    # loop para aceitar novas conexões
    while True:
        client_socket, addr = server_socket.accept()
        # Cria e inicia uma nova thread para cuidar do novo cliente
        thread = threading.Thread(target=lidar_cliente, args=(client_socket,), daemon=True)
        thread.start()


if __name__ == "__main__":
    main()
