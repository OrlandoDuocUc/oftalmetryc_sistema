from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.infraestructure.utils.tables import Base

class Diagnostico(Base):
    __tablename__ = 'diagnosticos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_cie10 = Column(String(10), nullable=False)
    descripcion = Column(String(200), nullable=False)
    categoria = Column(String(100))
    created_at = Column(DateTime, default=func.now(), nullable=False)

    def __repr__(self):
        return f"<Diagnostico(codigo={self.codigo_cie10}, descripcion={self.descripcion})>"

    def to_dict(self):
        return {
            'id': self.id,
            'codigo_cie10': self.codigo_cie10,
            'descripcion': self.descripcion,
            'categoria': self.categoria,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }