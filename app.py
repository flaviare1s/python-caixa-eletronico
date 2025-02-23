import json
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Caminho do arquivo de usuários
USUARIOS_FILE = 'usuarios.json'

# Função para carregar os usuários do arquivo JSON
def carregar_usuarios():
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, 'r') as f:
            return json.load(f)
    else:
        return {}

# Função para salvar os usuários no arquivo JSON
def salvar_usuarios(usuarios):
    with open(USUARIOS_FILE, 'w') as f:
        json.dump(usuarios, f, indent=4)

# Página inicial
@app.route('/')
def home():
    return render_template("index.html")

# Cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        
        # Carregar usuários cadastrados
        usuarios = carregar_usuarios()

        # Verifica se o usuário já existe
        if usuario in usuarios:
            flash("O nome de usuário já existe. Escolha outro.", "danger")
            return redirect(url_for('cadastro'))

        # Verifica a força da senha (exemplo simples, pode ser mais complexo)
        if len(senha) < 4:
            flash("A senha deve ter pelo menos 4 caracteres.", "danger")
            return redirect(url_for('cadastro'))

        # Caso contrário, cria o novo usuário
        usuarios[usuario] = {'senha': senha}
        salvar_usuarios(usuarios)  # Função para salvar o novo usuário no arquivo ou banco de dados
        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for('login'))
    
    return render_template("cadastro.html")


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'tentativas' not in session:
        session['tentativas'] = {}

    MAX_TENTATIVAS = 3
    usuario = request.form.get('usuario') if request.method == 'POST' else None
    senha = request.form.get('senha') if request.method == 'POST' else None
    
    usuarios = carregar_usuarios()

    if usuario:
        # Verifica se a conta está bloqueada
        if usuario in session['tentativas'] and session['tentativas'][usuario].get('bloqueado', False):
            flash("Sua conta está bloqueada devido a múltiplas tentativas de login malsucedidas. Tente novamente mais tarde.", "danger")
            return redirect(url_for('login'))

        # Verifica se as credenciais são válidas
        if usuario in usuarios and usuarios[usuario]['senha'] == senha:
            session['tentativas'][usuario] = {'tentativas': 0, 'bloqueado': False}
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for('dashboard', usuario=usuario))
        else:
            # Incrementa as tentativas
            if usuario in session['tentativas']:
                session['tentativas'][usuario]['tentativas'] += 1
            else:
                session['tentativas'][usuario] = {'tentativas': 1, 'bloqueado': False}

            # Se o número máximo de tentativas for alcançado, bloqueia a conta
            if session['tentativas'][usuario]['tentativas'] >= MAX_TENTATIVAS:
                session['tentativas'][usuario]['bloqueado'] = True
                flash("Número máximo de tentativas atingido. Sua conta foi bloqueada.", "danger")
            else:
                flash(f"Credenciais inválidas. Tentativas restantes: {MAX_TENTATIVAS - session['tentativas'][usuario]['tentativas']}", "danger")
            
            return redirect(url_for('login'))
    
    return render_template("login.html")

# Dashboard
@app.route('/dashboard/<usuario>')
def dashboard(usuario):
    usuarios = carregar_usuarios()
    if usuario not in usuarios:
        return redirect(url_for('login'))
    
    return render_template("dashboard.html", usuario=usuario)


# Ver Saldo
@app.route('/ver_saldo/<usuario>')
def ver_saldo(usuario):
    usuarios = carregar_usuarios()
    if usuario not in usuarios:
        return redirect(url_for('login'))
    saldo = usuarios[usuario]['saldo']
    return render_template("saldo.html", usuario=usuario, saldo=saldo)

# Alterar Senha
@app.route('/alterar_senha/<usuario>', methods=['GET', 'POST'])
def alterar_senha(usuario):
    usuarios = carregar_usuarios()
    
    if usuario not in usuarios:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nova_senha = request.form['nova_senha']
        usuarios[usuario]['senha'] = nova_senha
        salvar_usuarios(usuarios)
        flash("Senha alterada com sucesso!", "success")
        return redirect(url_for('dashboard', usuario=usuario))
    
    return render_template("alterar_senha.html", usuario=usuario)

# Extrato
@app.route('/extrato/<usuario>')
def extrato(usuario):
    usuarios = carregar_usuarios()
    if usuario not in usuarios:
        return redirect(url_for('login'))
    
    extrato = usuarios[usuario].get('extrato', [])
    return render_template("extrato.html", usuario=usuario, extrato=extrato)

# Saque
@app.route('/saque/<usuario>', methods=['GET', 'POST'])
def saque(usuario):
    usuarios = carregar_usuarios()
    
    if usuario not in usuarios:
        return redirect(url_for('login'))

    if request.method == 'POST':
        valor = float(request.form['valor'])
        if valor <= 0:
            flash("Valor inválido.", "danger")
        elif valor > usuarios[usuario]['saldo']:
            flash("Saldo insuficiente.", "danger")
        else:
            usuarios[usuario]['saldo'] -= valor
            data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            usuarios[usuario]['extrato'].append(f"Saque: R${valor:.2f} - Data/Hora: {data_hora}")
            salvar_usuarios(usuarios)
            flash("Saque realizado com sucesso!", "success")
        return redirect(url_for('dashboard', usuario=usuario))
    
    return render_template("saque.html", usuario=usuario)

# Depósito
@app.route('/deposito/<usuario>', methods=['GET', 'POST'])
def deposito(usuario):
    usuarios = carregar_usuarios()
    
    if usuario not in usuarios:
        return redirect(url_for('login'))

    if request.method == 'POST':
        valor = float(request.form['valor'])
        if valor <= 0:
            flash("Valor inválido.", "danger")
        else:
            usuarios[usuario]['saldo'] += valor
            data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            usuarios[usuario]['extrato'].append(f"Depósito: R${valor:.2f} - Data/Hora: {data_hora}")
            salvar_usuarios(usuarios)
            flash("Depósito realizado com sucesso!", "success")
        return redirect(url_for('dashboard', usuario=usuario))

    return render_template("deposito.html", usuario=usuario)

# Transferência
@app.route('/transferencia/<usuario>', methods=['GET', 'POST'])
def transferencia(usuario):
    usuarios = carregar_usuarios()
    
    if usuario not in usuarios:
        return redirect(url_for('login'))

    if request.method == 'POST':
        destinatario = request.form['destinatario']
        valor = float(request.form['valor'])
        if destinatario not in usuarios:
            flash("Destinatário não encontrado.", "danger")
        elif valor <= 0:
            flash("Valor inválido.", "danger")
        elif valor > usuarios[usuario]['saldo']:
            flash("Saldo insuficiente.", "danger")
        else:
            usuarios[usuario]['saldo'] -= valor
            usuarios[destinatario]['saldo'] += valor
            data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            usuarios[usuario]['extrato'].append(f"Transferência enviada: R${valor:.2f} para {destinatario} - Data/Hora: {data_hora}")
            usuarios[destinatario]['extrato'].append(f"Transferência recebida: R${valor:.2f} de {usuario} - Data/Hora: {data_hora}")
            salvar_usuarios(usuarios)
            flash(f"Transferência de R${valor:.2f} realizada com sucesso para {destinatario}!", "success")
        return redirect(url_for('dashboard', usuario=usuario))

    return render_template("transferencia.html", usuario=usuario)

# Logout
@app.route('/logout')
def logout():
    # Limpar a sessão ou qualquer dado relacionado ao usuário logado
    return redirect(url_for('login'))

# Executa o aplicativo
if __name__ == '__main__':
    app.run(debug=True)
