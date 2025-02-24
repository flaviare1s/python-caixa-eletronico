from flask import Flask, render_template, request, redirect, url_for
import datetime

app = Flask(__name__)

# Variáveis de controle
saldo = 10
senha = "1234"
limite_saque = 1000
saques_realizados = 0
tentativas = 3
extrato = []

@app.route('/')
def index():
    return render_template('index.html', saldo=saldo, extrato=extrato)

@app.route('/autenticar', methods=['POST'])
def autenticar_usuario():
    global tentativas
    senha_digitada = request.form['senha']
    if senha_digitada == senha:
        return redirect(url_for('menu'))
    else:
        tentativas -= 1
        if tentativas > 0:
            return f"Senha incorreta. Você tem {tentativas} tentativas restantes."
        else:
            return "Número de tentativas excedido. Acesso bloqueado."

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/verificar_saldo')
def verificar_saldo():
    return render_template('index.html', saldo=saldo, extrato=extrato)

@app.route('/ver_extrato')
def ver_extrato():
    return render_template('extrato.html', extrato=extrato)

@app.route('/depositar', methods=['POST'])
def depositar():
    global saldo
    valor_deposito = float(request.form['valor_deposito'])
    if valor_deposito > 0:
        saldo += valor_deposito
        data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        extrato.append(f"Depósito: R${valor_deposito:.2f} - Data/Hora: {data_hora}")
    return redirect(url_for('verificar_saldo'))

@app.route('/sacar', methods=['POST'])
def sacar():
    global saldo, saques_realizados
    valor = float(request.form['valor_saque'])
    if valor <= 0:
        return "Valor inválido para saque"
    elif valor > saldo:
        return "Saldo insuficiente"
    elif saques_realizados + valor > limite_saque:
        return "Limite de saque excedido"
    else:
        saldo -= valor
        saques_realizados += valor
        data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        extrato.append(f"Saque: R${valor:.2f} - Data/Hora: {data_hora}")
    return redirect(url_for('verificar_saldo'))

if __name__ == '__main__':
    app.run(debug=True)
