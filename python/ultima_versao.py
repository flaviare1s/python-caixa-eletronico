import datetime
import json
import os

ARQUIVO_DADOS = "usuarios.json"

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r") as file:
            return json.load(file)
    return {
        "user1": {"senha": "1234", "saldo": 100, "extrato": [], "saques_realizados": 0, "total_sacado": 0},
        "user2": {"senha": "5678", "saldo": 200, "extrato": [], "saques_realizados": 0, "total_sacado": 0},
        "user3": {"senha": "abcd", "saldo": 300, "extrato": [], "saques_realizados": 0, "total_sacado": 0}
    }

def salvar_dados():
    with open(ARQUIVO_DADOS, "w") as file:
        json.dump(usuarios, file, indent=4)

usuarios = carregar_dados()
usuario_atual = None
limite_saque = 1000
usuarios_bloqueados = {}

def cadastrar_usuario():
    usuario = input("Digite o nome de usuário para cadastro: ")
    if usuario in usuarios:
        print("Usuário já existe. Escolha outro nome.")
        return
    senha = input("Digite a senha para o novo usuário: ")
    usuarios[usuario] = {
        "senha": senha,
        "saldo": 0,
        "extrato": [],
        "saques_realizados": 0,
        "total_sacado": 0
    }
    salvar_dados()
    print("Usuário cadastrado com sucesso!")

def autenticar_usuario():
    global usuario_atual
    tentativas = 3

    while tentativas > 0:
        usuario = input("Digite seu nome de usuário: ")
        if usuario in usuarios:
            senha_digitada = input("Digite a senha: ")
            if senha_digitada == usuarios[usuario]["senha"]:
                print("Acesso permitido!")
                usuario_atual = usuario
                return True
            else:
                tentativas -= 1
                print(f"Senha incorreta. Você tem {tentativas} tentativas restantes.")
        else:
            print("Usuário não encontrado.")

    print("Número de tentativas excedido. Acesso bloqueado.")
    return False

def verificar_saldo():
    print(f"Seu saldo é de R${usuarios[usuario_atual]['saldo']:.2f}")

def depositar():
    valor_deposito = float(input("Digite o valor a ser depositado: "))
    if valor_deposito > 0:
        usuarios[usuario_atual]["saldo"] += valor_deposito
        data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        usuarios[usuario_atual]["extrato"].append(f"Depósito: R${valor_deposito:.2f} - Data/Hora: {data_hora}")
        salvar_dados()
        print("Depósito realizado com sucesso!")
        verificar_saldo()
    else:
        print("Valor de depósito inválido. O valor deve ser maior que zero.")

def sacar():
    valor = float(input("Digite o valor a ser sacado: "))
    if valor <= 0:
        print("Valor inválido para saque")
    elif valor > usuarios[usuario_atual]["saldo"]:
        print("Saldo insuficiente")
    elif usuarios[usuario_atual]["total_sacado"] + valor > limite_saque:
        print(f"Você já sacou R${usuarios[usuario_atual]['total_sacado']:.2f} hoje. O limite diário é de R${limite_saque:.2f}.")
    else:
        usuarios[usuario_atual]["saldo"] -= valor
        usuarios[usuario_atual]["saques_realizados"] += 1
        usuarios[usuario_atual]["total_sacado"] += valor
        data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        usuarios[usuario_atual]["extrato"].append(f"Saque: R${valor:.2f} - Data/Hora: {data_hora}")
        salvar_dados()
        print(f"Valor do Saque R${valor:.2f} realizado com sucesso!")
        verificar_saldo()

def transferir():
    destinatario = input("Digite o nome do usuário destinatário: ")
    if destinatario not in usuarios:
        print("Usuário destinatário não encontrado.")
        return

    valor = float(input("Digite o valor a ser transferido: "))
    if valor <= 0:
        print("Valor inválido para transferência.")
    elif valor > usuarios[usuario_atual]["saldo"]:
        print("Saldo insuficiente para transferência.")
    else:
        usuarios[usuario_atual]["saldo"] -= valor
        usuarios[destinatario]["saldo"] += valor
        data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        usuarios[usuario_atual]["extrato"].append(f"Transferência enviada: R${valor:.2f} para {destinatario} - Data/Hora: {data_hora}")
        usuarios[destinatario]["extrato"].append(f"Transferência recebida: R${valor:.2f} de {usuario_atual} - Data/Hora: {data_hora}")
        salvar_dados()
        print(f"Transferência de R${valor:.2f} realizada com sucesso para {destinatario}!")
        verificar_saldo()

def ver_extrato():
    print("\nExtrato:")
    if not usuarios[usuario_atual]["extrato"]:
        print("Nenhuma transação registrada.")
    else:
        for transacao in usuarios[usuario_atual]["extrato"]:
            print(transacao)
    print(f"Seu saldo é de R${usuarios[usuario_atual]['saldo']:.2f}")

def alterar_senha():
    senha_atual = input("Digite a senha atual: ")
    if senha_atual == usuarios[usuario_atual]["senha"]:
        nova_senha = input("Digite a nova senha: ")
        usuarios[usuario_atual]["senha"] = nova_senha
        salvar_dados()
        print("Senha alterada com sucesso!")
    else:
        print("Senha atual incorreta.")

def menu():
    global usuario_atual
    print("Bem-vindo ao Simulador de Caixa Eletrônico!")

    while True:
        print("\n1. Cadastrar Novo Usuário")
        print("2. Entrar no Sistema (Login)")
        print("3. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            if autenticar_usuario():
                break
        elif opcao == "3":
            print("Saindo do sistema. Obrigado!")
            return
        else:
            print("Opção inválida! Tente novamente.")

    while True:
        print("\nSelecione uma das opções abaixo!")
        print("\n1. Ver Saldo")
        print("2. Depositar")
        print("3. Sacar")
        print("4. Ver Extrato")
        print("5. Alterar Senha")
        print("6. Transferir Valor")
        print("7. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            verificar_saldo()
        elif opcao == "2":
            depositar()
        elif opcao == "3":
            sacar()
        elif opcao == "4":
            ver_extrato()
        elif opcao == "5":
            alterar_senha()
        elif opcao == "6":
            transferir()
        elif opcao == "7":
            print("Saindo do sistema. Obrigado!")
            break
        else:
            print("Opção inválida! Tente novamente.")

menu()
