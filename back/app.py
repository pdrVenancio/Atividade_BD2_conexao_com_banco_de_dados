from urllib.parse import quote_plus
from flask import Flask, send_from_directory
from flask_cors import CORS  # Adicionar
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

app = Flask(__name__, static_folder='../front', static_url_path='')
CORS(app)

# URI de conexão com o banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg://postgres:3081@localhost:5432/northwind'

# Inicializando o SQLAlchemy
db = SQLAlchemy(app)

# Criando o engine do SQLAlchemy para criar sessões de banco
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

# Criando a sessão global para uso no DAO
Session = sessionmaker(bind=engine)

# Função que registra blueprints
def create_app():
    from api.reports import reports_bp 
    from api.orders import orders_bp  
    from api.orders_details import orders_details_bp  
    from api.products import product_bp  
    from api.customers import customers_bp  
    from api.employeeid import employee_bp  
    from api.shippers import shipp_bp  

    app.register_blueprint(reports_bp)
    app.register_blueprint(orders_bp )
    app.register_blueprint(orders_details_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(shipp_bp)
    
    return  app

# Inicializando a aplicação
if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
        
    app = create_app()
    app.run(debug=True)
