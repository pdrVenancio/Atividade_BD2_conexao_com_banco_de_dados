class BaseModel:
    # Classe base com métodos comuns a todos os modelos
    
    def to_dict(self):
        # Converte o objeto para dicionário
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}