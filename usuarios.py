import datetime

usuarios = {}

def cadastrar_usuario():
    usuario = input("Digite o nome de usuário: ")
    if usuario in usuarios:
        print("Usuário já existe!")
        return
    senha = input("Digite a senha: ")
    usuarios[usuario] = {
        'senha': senha,
        'saldo': 10,
        'limite_saque': 1000,
        'saques_realizados': 0,
        'extrato': []
    }
    print("Usuário cadastrado com sucesso!")

def autenticar_usuario():
    usuario = input("Digite o nome de usuário: ")
    if usuario not in usuarios:
        print("Usuário não encontrado!")
        return None
    tentativas = 3
    while tentativas > 0:
        senha_digitada = input("Digite a senha: ")
        if senha_digitada == usuarios[usuario]['senha']:
            print("Acesso permitido!")
            return usuario
        else:
            tentativas -= 1
            print(f"Senha incorreta. Você tem {tentativas} tentativas restantes.")
    print("Número de tentativas excedido. Acesso bloqueado.")
    return None

def verificar_saldo(usuario):
    print(f"Seu saldo é de R${usuarios[usuario]['saldo']:.2f}")

def depositar(usuario):
    valor_deposito = float(input("Digite o valor a ser depositado: "))
    if valor_deposito > 0:
        usuarios[usuario]['saldo'] += valor_deposito
        data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        usuarios[usuario]['extrato'].append(f"Depósito: R${valor_deposito:.2f} - Data/Hora: {data_hora}")
    else:
        print("Valor de depósito inválido. O valor deve ser maior que zero.")

def sacar(usuario):
    print(f'Saldo Inicial: {usuarios[usuario]["saldo"]}')
    valor = float(input("Digite o valor a ser sacado: "))
    if valor <= 0:
        print('Valor inválido para saque')
    elif valor > usuarios[usuario]['saldo']:
        print('Saldo insuficiente')
    elif usuarios[usuario]['saques_realizados'] + valor > usuarios[usuario]['limite_saque']:
        print('Limite de saque excedido')
    else:
        usuarios[usuario]['saldo'] -= valor
        usuarios[usuario]['saques_realizados'] += valor
        data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        usuarios[usuario]['extrato'].append(f"Saque: R${valor:.2f} - Data/Hora: {data_hora}")
        print(f"Valor do Saque R${valor:.2f} Realizado com sucesso!")

def ver_extrato(usuario):
    print("\nExtrato:")
    if not usuarios[usuario]['extrato']:
        print("Nenhuma transação registrada.")
    else:
        for transacao in usuarios[usuario]['extrato']:
            print(transacao)

def alterar_senha(usuario):
    senha_atual = input("Digite a senha atual: ")
    if senha_atual == usuarios[usuario]['senha']:
        nova_senha = input("Digite a nova senha: ")
        usuarios[usuario]['senha'] = nova_senha
        print("Senha alterada com sucesso!")
    else:
        print('Senha Atual Incorreta.')

def menu():
    while True:
        print("\nBem-vindo ao Simulador de Caixa Eletrônico!")
        print("1. Cadastrar novo usuário")
        print("2. Entrar")
        print("3. Sair")
        opcao = input("Digite o número da opção desejada: ")
        
        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            usuario = autenticar_usuario()
            if usuario:
                while True:
                    print("\nEscolha uma opção:")
                    print("1. Verificar Saldo")
                    print("2. Depositar")
                    print("3. Sacar")
                    print("4. Ver Extrato")
                    print("5. Alterar Senha")
                    print("6. Sair")

                    opcao = input("Digite o número da opção desejada: ")
                    if opcao == "1":
                        verificar_saldo(usuario)
                    elif opcao == "2":
                        depositar(usuario)
                    elif opcao == "3":
                        sacar(usuario)
                    elif opcao == "4":
                        ver_extrato(usuario)
                    elif opcao == "5":
                        alterar_senha(usuario)
                    elif opcao == "6":
                        print("Saindo do sistema. Obrigado(a)!")
                        break
                    else:
                        print('Opção inválida!')
        elif opcao == "3":
            print("Saindo do sistema. Obrigado(a)!")
            break
        else:
            print('Opção inválida!')

menu()
