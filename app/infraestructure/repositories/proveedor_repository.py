from app.domain.models.proveedor import Proveedor
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

class ProveedorRepository:
    """
    Repositorio para operaciones CRUD de proveedores
    """
    
    def __init__(self, session: Session):
        self.session = session
    
    def save(self, proveedor: Proveedor) -> bool:
        """Guarda un proveedor en la base de datos"""
        try:
            self.session.add(proveedor)
            self.session.commit()
            self.session.refresh(proveedor)
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error al guardar proveedor: {e}")
            return False
    
    def get_all(self) -> List[Proveedor]:
        """Obtiene todos los proveedores activos"""
        try:
            return self.session.query(Proveedor)\
                .filter(Proveedor.estado == True)\
                .order_by(Proveedor.razon_social.asc())\
                .all()
        except Exception as e:
            print(f"Error al obtener proveedores: {e}")
            return []
    
    def get_by_id(self, proveedor_id: int) -> Optional[Proveedor]:
        """Obtiene un proveedor por su ID"""
        try:
            return self.session.query(Proveedor)\
                .filter(Proveedor.proveedor_id == proveedor_id)\
                .first()
        except Exception as e:
            print(f"Error al obtener proveedor por ID: {e}")
            return None
    
    def get_by_codigo(self, codigo: str) -> Optional[Proveedor]:
        """Obtiene un proveedor por su código"""
        try:
            return self.session.query(Proveedor)\
                .filter(Proveedor.codigo_proveedor == codigo)\
                .first()
        except Exception as e:
            print(f"Error al obtener proveedor por código: {e}")
            return None
    
    def get_by_rut(self, rut: str) -> Optional[Proveedor]:
        """Obtiene un proveedor por su RUT"""
        try:
            return self.session.query(Proveedor)\
                .filter(Proveedor.rut == rut)\
                .first()
        except Exception as e:
            print(f"Error al obtener proveedor por RUT: {e}")
            return None
    
    def search(self, term: str) -> List[Proveedor]:
        """Busca proveedores por término en razón social, nombre comercial o RUT"""
        try:
            search_term = f"%{term.lower()}%"
            return self.session.query(Proveedor)\
                .filter(
                    Proveedor.estado == True,
                    (func.lower(Proveedor.razon_social).like(search_term) |
                     func.lower(Proveedor.nombre_comercial).like(search_term) |
                     func.lower(Proveedor.rut).like(search_term) |
                     func.lower(Proveedor.codigo_proveedor).like(search_term))
                )\
                .order_by(Proveedor.razon_social.asc())\
                .all()
        except Exception as e:
            print(f"Error al buscar proveedores: {e}")
            return []
    
    def update(self, proveedor: Proveedor) -> bool:
        """Actualiza un proveedor existente"""
        try:
            self.session.merge(proveedor)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error al actualizar proveedor: {e}")
            return False
    
    def delete(self, proveedor_id: int) -> bool:
        """Desactiva un proveedor (soft delete)"""
        try:
            proveedor = self.get_by_id(proveedor_id)
            if proveedor:
                proveedor.estado = False
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            print(f"Error al eliminar proveedor: {e}")
            return False
    
    def get_by_categoria(self, categoria: str) -> List[Proveedor]:
        """Obtiene proveedores que manejan una categoría específica"""
        try:
            return self.session.query(Proveedor)\
                .filter(
                    Proveedor.estado == True,
                    Proveedor.categoria_productos.like(f"%{categoria}%")
                )\
                .order_by(Proveedor.razon_social.asc())\
                .all()
        except Exception as e:
            print(f"Error al obtener proveedores por categoría: {e}")
            return []
    
    def get_statistics(self) -> dict:
        """Obtiene estadísticas de proveedores"""
        try:
            total = self.session.query(Proveedor).filter(Proveedor.estado == True).count()
            con_email = self.session.query(Proveedor)\
                .filter(Proveedor.estado == True, Proveedor.email.isnot(None)).count()
            con_telefono = self.session.query(Proveedor)\
                .filter(Proveedor.estado == True, Proveedor.telefono.isnot(None)).count()
            con_representante = self.session.query(Proveedor)\
                .filter(Proveedor.estado == True, Proveedor.representante_nombre.isnot(None)).count()
            
            return {
                'total_proveedores': total,
                'con_email': con_email,
                'con_telefono': con_telefono,
                'con_representante': con_representante,
                'porcentaje_contacto_completo': (con_email / total * 100) if total > 0 else 0
            }
        except Exception as e:
            print(f"Error al obtener estadísticas: {e}")
            return {
                'total_proveedores': 0,
                'con_email': 0,
                'con_telefono': 0,
                'con_representante': 0,
                'porcentaje_contacto_completo': 0
            }