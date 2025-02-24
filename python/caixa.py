import datetime

saldo = 10
senha = "1234"
limite_saque = 1000
saques_realizados = 0
tentativas = 3
extrato = []

def autenticar_usuario():
    global tentativas  # Para poder modificar a variável tentativas dentro da função
    while tentativas > 0:
        senha_digitada = input("Digite a senha: ")
        if senha_digitada == senha:
            print("Acesso permitido!")
            return True
        else:
            tentativas -= 1  # Decrementa o número de tentativas
            print(f"Senha incorreta. Você tem {tentativas} tentativas restantes.")

    print("Número de tentativas excedido. Acesso bloqueado.")
    return False

def verificar_saldo():
    print(f"Seu saldo é de R${saldo:.2f}")

def depositar():
    global saldo
    valor_deposito = float(input("Digite o valor a ser depositado: "))
    if valor_deposito > 0:
        saldo += valor_deposito
        data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        extrato.append(f"Depósito: R${valor_deposito:.2f} - Data/Hora: {data_hora}")
    else:
        print("Valor de depósito inválido. O valor deve ser maior que zero.")

def sacar():
    global saldo,saques_realizados
    print(f'Saldo Inicial: {saldo}')
    valor = float(input("Digite o valor a ser sacado: "))
    if valor <= 0:
      print('Valor inválido para saque')
    elif valor > saldo:
      print('Saldo insuficiente')
    elif  saques_realizados + valor > limite_saque:
      print('limite de saque excedido')
    else:
      saldo -= valor
      saques_realizados += valor
      data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      extrato.append(f"Saque: R${valor:.2f} - Data/Hora: {data_hora}")
      print(f" Valor do Saque R${valor:.2f} Realizado com sucesso!")

def ver_extrato():
    print("\nExtrato:")
    if not extrato:
        print("Nenhuma transação registrada.")
    else:
      for transacao in extrato:
        print(transacao)

def alterar_senha():
    global senha
    senha_atual = input("Digite a senha atual: ")
    if senha_atual == senha:
        nova_senha = input("Digite a nova senha: ")
        senha = nova_senha
        print("Senha alterada com sucesso!")
    else:
      print('Senha Atual Incorreta.')

def menu():
    print("\nBem-vindo ao Simulador de Caixa Eletrônico!")
    if not autenticar_usuario():
        return
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
          print("Saindo do sistema. Obrigado(a)!")
          break
        else:
          print('Opção inválida!')

menu()
