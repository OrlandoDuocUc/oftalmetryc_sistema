from sqlalchemy import Column, BigInteger, String, DateTime, CHAR, ForeignKey
from app.infraestructure.utils.tables import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'usuario'

    usuario_id = Column(BigInteger, primary_key=True, autoincrement=True)
    rol_id = Column(BigInteger, ForeignKey('rol.rol_id'), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    nombre = Column(String(100), nullable=False)
    ap_pat = Column(String(100), nullable=False)
    ap_mat = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=True)
    estado = Column(CHAR(1), default='A', nullable=False)  # A=Activo, I=Inactivo

    def __repr__(self):
        return f"<User(nombre={self.nombre}, username={self.username}, estado={self.estado})>"
