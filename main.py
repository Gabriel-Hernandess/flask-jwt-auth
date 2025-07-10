from flask import Flask, jsonify, request
import jwt
import os
from datetime import datetime, timedelta

# Chave secreta para encriptação do token JWT
SECRET_KEY = "sua_chave_secreta"

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Bem-vindo ao auth com JWT via Flask!")

@app.route('/login', methods=["POST"])
def login():
    data = request.get_json()

    # Validação básica do corpo da requisição
    if not data:
        return jsonify(message="Dados não fornecidos!"), 400

    if 'username' not in data or 'password' not in data:
        return jsonify(message="Nome de usuário ou senha não definidos"), 400

    # Verificação de credenciais (exemplo simples, sem banco de dados)
    if data['username'] == 'admin' and data['password'] == '1234':
        # Define o tempo de expiração do token (60 minutos a partir de agora)
        exp = datetime.utcnow() + timedelta(minutes=60)
        exp_timestamp = int(exp.timestamp())  # JWT exige timestamp (int)

        # Gera o token com os dados do usuário e expiração
        token = jwt.encode(
            {
                'user': data['username'],
                'exp': exp_timestamp  # campo padrão para expiração
            },
            SECRET_KEY,
            algorithm='HS256'
        )

        return jsonify(token=token), 200

    return jsonify(message="Credenciais inválidas!"), 401

@app.route("/dados", methods=["GET"])
def dados():
    # Recupera o token do cabeçalho Authorization: Bearer <token>
    header = request.headers.get("Authorization")
    if not header:
        return jsonify(message="Token é necessário!"), 403

    parts = header.split()
    if parts[0].lower() != 'bearer' or len(parts) != 2:
        return jsonify(message="Cabeçalho de autorização incorreto!"), 401

    token = parts[1]

    try:
        # Decodifica e valida o token usando a chave secreta
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify(message=f"Bem-vindo, {decoded['user']}!"), 200

    except jwt.ExpiredSignatureError:
        return jsonify(message="Token expirado! Faça login novamente."), 401

    except jwt.InvalidTokenError:
        return jsonify(message="Token inválido!"), 403

if __name__ == '__main__':
    app.run(debug=True)
