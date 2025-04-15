from urllib.parse import quote_plus
from flask import Flask, send_from_directory
from flask_cors import CORS  # Adicionar
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

app = Flask(__name__, static_folder='../front', static_url_path='')
CORS(app)  # Adicionar esta linha

# URI de conexão com o banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg://postgres:root@localhost/northwind'

# Inicializando o SQLAlchemy
db = SQLAlchemy(app)

# Criando o engine do SQLAlchemy para criar sessões de banco
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

# Criando a sessão global para uso no DAO
Session = sessionmaker(bind=engine)

# Função que registra blueprints
def create_app():
    from api.reports import reports_bp  # Importação movida para dentro da função
    app.register_blueprint(reports_bp)
    return app

# Rota principal: carrega o index.html da pasta do front
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Rota para servir arquivos estáticos como style.css, script.js etc.
@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

# Inicializando a aplicação
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas, se necessário

    app = create_app()
    app.run(debug=True)
