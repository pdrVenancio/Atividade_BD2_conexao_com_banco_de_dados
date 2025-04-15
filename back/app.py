from urllib.parse import quote_plus
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



# Configure a URI de conexão
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg://postgres:root@localhost/postgres'

# Inicializando o SQLAlchemy
db = SQLAlchemy(app)

# Criando o engine do SQLAlchemy para criar sessões de banco
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

# Criando a sessão global para uso no DAO
Session = sessionmaker(bind=engine)

# Registrando o blueprint dentro da função create_app
def create_app():
    from api.reports import reports_bp  # Mova a importação para dentro da função
    from api.orders import orders_bp  
    from api.orders_details import orders_details_bp  

    app.register_blueprint(reports_bp)
    app.register_blueprint(orders_bp )
    app.register_blueprint(orders_details_bp)
    return app

@app.route('/')
def home():
    return "Bem-vindo ao sistema de relatórios!"

# Inicializando a aplicação
if __name__ == '__main__':
    # Criar as tabelas no banco de dados, se não existirem, dentro do contexto da aplicação
    with app.app_context():
        db.create_all()

    # Iniciando a aplicação
    app = create_app()
    app.run(debug=True)
