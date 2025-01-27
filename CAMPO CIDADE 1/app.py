from flask import Flask, request, redirect, url_for, flash, session, jsonify, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

# Configuração do Flask
app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_segura'
DATABASE = 'database.db'

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Inicialização do Banco de Dados
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            numero_telefone TEXT NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Templates HTML como strings
index_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Campo Cidade</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <header class="bg-success text-white py-3">
        <div class="container d-flex justify-content-between align-items-center">
            <a class="navbar-brand fw-bold" href="/">CAMPO CIDADE</a>
            <nav>
                <ul class="nav">
                    <li class="nav-item"><a class="nav-link text-white" href="/login">Login</a></li>
                    <li class="nav-item"><a class="nav-link text-white" href="#sobre">Sobre</a></li>
                    <li class="nav-item"><a class="nav-link text-white" href="#servicos">Serviços</a></li>
                    <li class="nav-item"><a class="nav-link text-white" href="#cadastro">Cadastro</a></li>
                </ul>
            </nav>
        </div>
    </header>
    <main class="container mt-5 pt-5">
        <h1>Bem-vindo ao Campo Cidade</h1>
        <p>Sistema de gerenciamento agrícola para pequenos produtores.</p>
        <div id="dashboard"></div>
    </main>
    <script>
        // Funções de animações (animame_index.js)
        function smoothScroll() {
            document.querySelectorAll('a.nav-link').forEach(link => {
                link.addEventListener('click', function(event) {
                    event.preventDefault();
                    const targetId = this.getAttribute('href').substring(1);
                    const targetSection = document.getElementById(targetId);

                    if (targetSection) {
                        targetSection.scrollIntoView({
                            behavior: 'smooth'
                        });
                    }
                });
            });
        }
        window.addEventListener('DOMContentLoaded', smoothScroll);
    </script>
</body>
</html>"""

login_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h2>Login</h2>
        <form method="POST" action="/login">
            <div class="mb-3">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" class="form-control" required>
            </div>
            <div class="mb-3">
                <label for="senha">Senha</label>
                <input type="password" id="senha" name="senha" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-primary">Entrar</button>
        </form>
    </div>
</body>
</html>"""

controle_de_producao_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Controle de Produção</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <header class="bg-success text-white py-3">
        <div class="container">
            <h1>Controle de Produção</h1>
        </div>
    </header>
    <main class="container mt-5">
        <div id="dashboard">
            <!-- Conteúdo gerado dinamicamente -->
        </div>
    </main>
</body>
</html>"""

# Rota inicial
@app.route('/')
def home():
    return render_template_string(index_html)

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        if user and check_password_hash(user['senha'], senha):
            session['user_id'] = user['id']
            flash('Login realizado com sucesso!', 'success')
            return redirect('/dashboard')
        else:
            flash('Credenciais inválidas!', 'danger')
    return render_template_string(login_html)

# Rota do dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Faça login para acessar o painel.', 'warning')
        return redirect('/login')
    return render_template_string(controle_de_producao_html)

# Rota de cadastro
@app.route('/cadastro', methods=['POST'])
def cadastro():
    data = request.json
    nome = data.get('nome')
    cpf = data.get('cpf')
    email = data.get('email')
    numero_telefone = data.get('numero_telefone')
    senha = generate_password_hash(data.get('senha'))
    if not all([nome, cpf, email, numero_telefone, senha]):
        return jsonify({'error': 'Preencha todos os campos!'}), 400

    try:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO users (nome, cpf, email, numero_telefone, senha) VALUES (?, ?, ?, ?, ?)',
            (nome, cpf, email, numero_telefone, senha)
        )
        conn.commit()
        conn.close()
        return jsonify({'success': 'Usuário cadastrado com sucesso!'})
    except sqlite3.IntegrityError as e:
        field = 'Email' if 'email' in str(e).lower() else 'CPF'
        return jsonify({'error': f'{field} já cadastrado!'}), 400

# Rota para logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Você saiu da conta.', 'info')
    return redirect('/')

# Inicializar banco de dados
if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
