from sqlalchemy import Column, BigInteger, String, DateTime, CHAR, Text
from app.infraestructure.utils.tables import Base
from datetime import datetime

class Cliente(Base):
    __tablename__ = 'cliente'

    cliente_id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombres = Column(String(100), nullable=False)
    ap_pat = Column(String(100), nullable=False)
    ap_mat = Column(String(100), nullable=True)
    email = Column(Text, nullable=True)
    telefono = Column(String(20), nullable=True)
    direccion = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=True)
    estado = Column(CHAR(1), default='A', nullable=False)  # A=Activo, I=Inactivo

    def __repr__(self):
        return f"<Cliente(nombres={self.nombres}, ap_pat={self.ap_pat}, estado={self.estado})>" 