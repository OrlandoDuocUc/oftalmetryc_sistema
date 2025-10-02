from sqlalchemy import Column, Integer, String, Date, Text, DateTime, func
from app.infraestructure.utils.tables import Base
from datetime import datetime

class Paciente(Base):
    __tablename__ = 'pacientes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rut = Column(String(12), unique=True, nullable=True)
    ci = Column(String(20), nullable=True)  # NUEVO: Cédula Ecuador
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    nombres = Column(String(100), nullable=True)  # NUEVO: Nombres separados
    apellidos = Column(String(100), nullable=True)  # NUEVO: Apellidos separados
    fecha_nacimiento = Column(Date)
    edad = Column(Integer)  # NUEVO: Edad calculada
    telefono = Column(String(20))
    email = Column(String(100))
    direccion = Column(Text)
    genero = Column(String(10))  # NUEVO: M/F/Otro
    ocupacion = Column(String(100))
    hobby = Column(String(200))  # NUEVO: Hobby del paciente
    contacto_emergencia = Column(String(100))
    telefono_emergencia = Column(String(20))
    observaciones = Column(Text)
    observaciones_generales = Column(Text)  # NUEVO: Observaciones generales
    estado = Column(String(20), default='Activo')  # NUEVO: Estado del paciente
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        documento = self.ci or self.rut
        return f"<Paciente(doc={documento}, nombre={self.nombre_completo})>"

    @property
    def nombre_completo(self):
        if self.nombres and self.apellidos:
            return f"{self.nombres} {self.apellidos}"
        else:
            return f"{self.nombre} {self.apellido}"
    
    @property
    def documento_identidad(self):
        """Retorna el documento de identidad (CI o RUT)"""
        return self.ci or self.rut
    
    def calcular_edad(self):
        """Calcula la edad basada en la fecha de nacimiento"""
        if self.fecha_nacimiento:
            today = datetime.today().date()
            return today.year - self.fecha_nacimiento.year - (
                (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
            )
        return None
    
    def to_dict(self):
        return {
            'id': self.id,
            'rut': self.rut,
            'ci': self.ci,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'nombre_completo': self.nombre_completo,
            'documento_identidad': self.documento_identidad,
            'fecha_nacimiento': self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None,
            'edad': self.edad,
            'telefono': self.telefono,
            'email': self.email,
            'direccion': self.direccion,
            'genero': self.genero,
            'ocupacion': self.ocupacion,
            'hobby': self.hobby,
            'contacto_emergencia': self.contacto_emergencia,
            'telefono_emergencia': self.telefono_emergencia,
            'observaciones': self.observaciones,
            'observaciones_generales': self.observaciones_generales,
            'estado': self.estado,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }