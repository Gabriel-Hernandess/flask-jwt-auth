from flask import Flask, jsonify, request
import jwt
import os
from datetime import datetime, timedelta

# Chave secreta para encriptação do token
SECRET_KEY = "sua_chave_secreta"

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Bem vindo ao auth com JWT via Flask!")

@app.route('/login', methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify(message="Dados não fornecidos!"), 400
    
    if 'username' not in data or 'password' not in data:
        return jsonify(message="Nome de usuario ou senha não definidos"), 400

    if data['username'] == 'admin' and data['password'] == '1234':
        # Gerar token jwt com tempo limite
        token = jwt.encode(
            {'user': data['username'], 'expiration': datetime.now() + timedelta(minutes=60)},
            SECRET_KEY,
            algorithm='HS256'
        )

        return jsonify(token=token)
    return jsonify(message="Credenciais inválidas!"), 401

@app.route("/dados", methods=["GET"])
def dados():
    # Obtém o token do cabeçalho da requisição
    header = request.headers.get("Authorization")
    if not header:
        return jsonify(message="Token é necessário!"), 403

    parts = header.split()
    if parts[0].lower() != 'bearer' or len(parts) != 2:
        return jsonify(message="Cabeçalho de autorização incorreto!"), 401
    token = parts[1]

    try:
        # Decodifica o token
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify(message=f"Bem-vindo, {decoded['user']}!")
    except jwt.ExpiredSignatureError:
        return jsonify(message="Token expirado! Faça login novamente."), 401
    except jwt.InvalidTokenError:
        return jsonify(message="Token inválido!"), 403

if __name__ == '__main__':
    app.run()
