from flask import Blueprint
from api.orders import orders_bp
from api.customers import customers_bp
from api.reports import reports_bp

def register_api(app):
    # Registrar os blueprints no aplicativo Flask
    app.register_blueprint(orders_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(reports_bp)
