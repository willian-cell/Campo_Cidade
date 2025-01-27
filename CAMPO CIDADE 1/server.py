import http.server
import socketserver
import sqlite3
from urllib.parse import parse_qs

# Configurações do banco de dados SQLite
DATABASE = 'database.db'

# Inicializa o banco de dados e cria a tabela, se não existir
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        # Lê o tamanho do conteúdo enviado
        content_length = int(self.headers['Content-Length'])
        # Lê os dados enviados no corpo da requisição
        post_data = self.rfile.read(content_length).decode('utf-8')
        # Processa os dados enviados no formato x-www-form-urlencoded
        data = parse_qs(post_data)

        nome = data.get('nome', [''])[0]
        email = data.get('email', [''])[0]
        senha = data.get('senha', [''])[0]

        if nome and email and senha:
            # Salva no banco de dados
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (nome, email, senha) VALUES (?, ?, ?)', (nome, email, senha))
            conn.commit()
            conn.close()

            # Retorna uma resposta de sucesso
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write('Dados salvos com sucesso!'.encode('utf-8'))
        else:
            # Retorna uma resposta de erro
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write('Erro: Dados inválidos!'.encode('utf-8'))


# Inicializa o banco de dados
init_db()

# Configura o servidor na porta 8000
PORT = 8000
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Servidor rodando na porta {PORT}")
    httpd.serve_forever()
