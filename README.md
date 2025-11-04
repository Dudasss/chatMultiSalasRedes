# 💬 Sistema de Chat com Sockets TCP (Cliente/Servidor)

Projeto desenvolvido para a disciplina de **Redes II** do curso de **Tecnologia em Análise e Desenvolvimento de Sistemas – IFBA Campus Irecê**.

Este sistema implementa um chat com múltiplas salas, utilizando **arquitetura cliente/servidor** e **comunicação via sockets TCP**.  
O objetivo é permitir a comunicação entre vários clientes conectados a um servidor central, garantindo a **entrega confiável das mensagens** e o **gerenciamento dinâmico de salas**.

---

## 🧩 Estrutura do Projeto
├── README.md
├── servidor/
│ ├── servidor.py
├── cliente/
│ ├── cliente.py


---

## ⚙️ Requisitos do Sistema

- **VirtualBox/WSL** (para integração entre as máquinas virtuais)
- **Linux Debian** (preferencial)
- **Python 3.10+**
- Ambas as VMs (cliente e servidor) devem estar na **mesma rede interna**

---

## 🚀 Como Compilar e Executar o Código

### 🔧 Passo 1: Clonar o repositório

```bash
git clone https://github.com/Dudasss/chatMultiSalasRedes.git
cd chatMultiSalasRedes
```

### 🖥️ Passo 2: Configurar o ambiente

Instale o Python (se ainda não estiver instalado):
```bash
sudo apt update
sudo apt install python3 python3-pip -y
```

### 🌐 Passo 3: Configurar a rede no VirtualBox

1. Crie duas VMs (uma para o servidor e outra para o cliente).

2. Configure ambas na mesma rede interna.

3. Descubra o IP de cada VM com o comando:
```bash
ip addr show
 ```

---
## 🖧 Execução do Servidor

Na máquina do servidor:
```bash
cd servidor
python3 servidor.py
```

- O servidor solicitará:

  - Endereço IP e porta para iniciar o serviço.

- Exemplo:
```bash
Informe o IP do servidor: 127.0.0.1
Informe a porta: 7856
Servidor iniciado em 127.0.0.1:7856
```
---
## 💻 Execução do Cliente

Na máquina cliente:
```bash
cd cliente
python3 cliente.py
```

O cliente solicitará:

- IP do servidor e porta

- Nome de usuário

Exemplo:
```bash
Informe o IP do servidor: 192.168.56.101
Informe a porta: 5000
Informe seu nome de usuário: Ana
Conectado ao servidor!
```
---

## 💬 Comandos Disponíveis no Cliente
| Comando                      | Descrição                                     |
| ---------------------------- | --------------------------------------------- |
| `/join #nome_sala`           | Entra ou cria uma nova sala                   |
| `/leave`                     | Sai da sala atual                             |
| `/private #usuario mensagem` | Envia uma mensagem privada para outro usuário |
| `/exit` ou `/quit`           | Encerra a conexão com o servidor              |

---

## 🧠 Funcionalidades Implementadas
🔹 Servidor

  - Solicita IP e porta na inicialização

  - Aceita múltiplos clientes simultaneamente

  - Gerencia salas de bate-papo dinamicamente

  - Transmite mensagens via broadcast para os membros da sala

  - Fecha conexões de forma segura com /exit

🔹 Cliente

  - Solicita IP e porta do servidor

  - Envia nome de usuário

  - Permite entrar/sair de salas

  - Suporta envio de mensagens e comandos

  - Encerra conexão com segurança
---
## 🧱 Tecnologias Utilizadas

 - Python 3

 - Sockets TCP (socket e threading)

 - VirtualBox/WSL + Debian Linux

 - Comunicação cliente-servidor via rede interna

---

## 👥 Autoria

 - Aluna: Eduarda Samanta

 - Professor: Renan Felipe

 - Disciplina: Redes II

 - Instituição: IFBA – Campus Irecê
