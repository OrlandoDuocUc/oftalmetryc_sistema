from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey, func, Numeric, BigInteger
from sqlalchemy.orm import relationship
from app.infraestructure.utils.tables import Base

class RecetaOftalmologica(Base):
    __tablename__ = 'recetas_oftalmologicas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    consulta_id = Column(Integer, ForeignKey('consultas_medicas.id', ondelete='CASCADE'), nullable=False)
    
    # Datos del Lente OD
    od_esfera = Column(Numeric(4,2))
    od_cilindro = Column(Numeric(4,2))
    od_eje = Column(Integer)
    od_add = Column(Numeric(4,2))
    od_prisma = Column(Numeric(3,1))
    od_base = Column(String(20))
    od_dp = Column(Numeric(4,1))  # Distancia pupilar
    
    # Datos del Lente OI
    oi_esfera = Column(Numeric(4,2))
    oi_cilindro = Column(Numeric(4,2))
    oi_eje = Column(Integer)
    oi_add = Column(Numeric(4,2))
    oi_prisma = Column(Numeric(3,1))
    oi_base = Column(String(20))
    oi_dp = Column(Numeric(4,1))
    
    # Información adicional
    tipo_lente = Column(String(50))  # monofocal, bifocal, progresivo
    material_lente = Column(String(50))  # orgánico, mineral, policarbonato
    filtros = Column(String(100))  # UV, antirreflex, fotocromático
    tipo_armazon = Column(String(50))  # completo, al aire, semi al aire
    
    observaciones_receta = Column(Text)
    fecha_entrega = Column(Date)
    vendedor_id = Column(BigInteger, ForeignKey('usuario.usuario_id'))
    estado = Column(String(20), default='pendiente')  # pendiente, en_proceso, entregado
    
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relaciones
    consulta = relationship("ConsultaMedica", foreign_keys=[consulta_id])

    def __repr__(self):
        return f"<RecetaOftalmologica(id={self.id}, consulta_id={self.consulta_id}, estado={self.estado})>"

    def to_dict(self):
        return {
            'id': self.id,
            'consulta_id': self.consulta_id,
            'od_esfera': float(self.od_esfera) if self.od_esfera else None,
            'od_cilindro': float(self.od_cilindro) if self.od_cilindro else None,
            'od_eje': self.od_eje,
            'od_add': float(self.od_add) if self.od_add else None,
            'od_prisma': float(self.od_prisma) if self.od_prisma else None,
            'od_base': self.od_base,
            'od_dp': float(self.od_dp) if self.od_dp else None,
            'oi_esfera': float(self.oi_esfera) if self.oi_esfera else None,
            'oi_cilindro': float(self.oi_cilindro) if self.oi_cilindro else None,
            'oi_eje': self.oi_eje,
            'oi_add': float(self.oi_add) if self.oi_add else None,
            'oi_prisma': float(self.oi_prisma) if self.oi_prisma else None,
            'oi_base': self.oi_base,
            'oi_dp': float(self.oi_dp) if self.oi_dp else None,
            'tipo_lente': self.tipo_lente,
            'material_lente': self.material_lente,
            'filtros': self.filtros,
            'tipo_armazon': self.tipo_armazon,
            'observaciones_receta': self.observaciones_receta,
            'fecha_entrega': self.fecha_entrega.isoformat() if self.fecha_entrega else None,
            'vendedor_id': self.vendedor_id,
            'estado': self.estado,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }