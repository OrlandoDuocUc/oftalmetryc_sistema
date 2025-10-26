# ===============================================================================
# REPOSITORIO - FICHA CLÍNICA DIGITAL
# Sistema: Oftalmetryc - Gestión de Fichas Clínicas
# Autor: Orlando Rodriguez
# Fecha: 2 de octubre de 2025
# ===============================================================================

"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, desc, func, extract
from datetime import datetime, date
import logging

from app.domain.models.ficha_clinica_models import PacienteV2, FichaClinica, ExamenOftalmologicoCompleto

logger = logging.getLogger(__name__)

# ===============================================================================
# REPOSITORIO PACIENTES V2
# ===============================================================================

class PacienteV2Repository:
    """
    Repositorio para gestionar operaciones CRUD de PacienteV2
    """
    
    def __init__(self, session: Session):
        self.session = session
    
    def crear_paciente(self, datos_paciente: Dict[str, Any]) -> PacienteV2:
        """
        Crea un nuevo paciente
        """
        try:
            paciente = PacienteV2(**datos_paciente)
            paciente.calcular_edad()  # Calcular edad automáticamente
            
            self.session.add(paciente)
            self.session.commit()
            self.session.refresh(paciente)
            
            logger.info(f"Paciente creado exitosamente: {paciente.ci}")
            return paciente
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error al crear paciente: {str(e)}")
            raise
    
    def obtener_por_id(self, paciente_id: int) -> Optional[PacienteV2]:
        """
        Obtiene un paciente por ID con sus fichas clínicas
        """
        return self.session.query(PacienteV2)\
            .options(joinedload(PacienteV2.fichas_clinicas))\
            .filter(PacienteV2.id == paciente_id)\
            .first()
    
    def obtener_por_ci(self, ci: str) -> Optional[PacienteV2]:
        """
        Obtiene un paciente por cédula de identidad
        """
        return self.session.query(PacienteV2)\
            .filter(PacienteV2.ci == ci)\
            .first()
    
    def buscar_pacientes(self, termino_busqueda: str) -> List[PacienteV2]:
        """
        Busca pacientes por CI, nombres o apellidos
        """
        termino = f"%{termino_busqueda.lower()}%"
        
        return self.session.query(PacienteV2)\
            .filter(
                or_(
                    PacienteV2.ci.ilike(termino),
                    PacienteV2.nombres.ilike(termino),
                    PacienteV2.apellidos.ilike(termino),
                    func.concat(PacienteV2.nombres, ' ', PacienteV2.apellidos).ilike(termino)
                )
            )\
            .filter(PacienteV2.estado == 'Activo')\
            .order_by(PacienteV2.nombres, PacienteV2.apellidos)\
            .all()
    
    def obtener_pacientes_recientes(self, limit: int = 10) -> List[PacienteV2]:
        """
        Obtiene los pacientes más recientemente visitados
        """
        return self.session.query(PacienteV2)\
            .join(FichaClinica)\
            .filter(PacienteV2.estado == 'Activo')\
            .order_by(desc(FichaClinica.fecha_consulta))\
            .limit(limit)\
            .all()
    
    def obtener_todos_paginado(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """
        Obtiene todos los pacientes de forma paginada
        """
        offset = (page - 1) * per_page
        
        total = self.session.query(PacienteV2)\
            .filter(PacienteV2.estado == 'Activo')\
            .count()
        
        pacientes = self.session.query(PacienteV2)\
            .filter(PacienteV2.estado == 'Activo')\
            .order_by(PacienteV2.nombres, PacienteV2.apellidos)\
            .offset(offset)\
            .limit(per_page)\
            .all()
        
        return {
            'pacientes': pacientes,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }
    
    def actualizar_paciente(self, paciente_id: int, datos_actualizados: Dict[str, Any]) -> Optional[PacienteV2]:
        """
        Actualiza los datos de un paciente
        """
        try:
            paciente = self.obtener_por_id(paciente_id)
            if not paciente:
                return None
            
            for key, value in datos_actualizados.items():
                if hasattr(paciente, key):
                    setattr(paciente, key, value)
            
            # Recalcular edad si cambió la fecha de nacimiento
            if 'fecha_nacimiento' in datos_actualizados:
                paciente.calcular_edad()
            
            self.session.commit()
            logger.info(f"Paciente actualizado: {paciente.ci}")
            return paciente
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error al actualizar paciente: {str(e)}")
            raise
    
    def desactivar_paciente(self, paciente_id: int) -> bool:
        """
        Desactiva un paciente (soft delete)
        """
        try:
            paciente = self.obtener_por_id(paciente_id)
            if not paciente:
                return False
            
            paciente.estado = 'Inactivo'
            self.session.commit()
            logger.info(f"Paciente desactivado: {paciente.ci}")
            return True
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error al desactivar paciente: {str(e)}")
            raise

# ===============================================================================
# REPOSITORIO FICHAS CLÍNICAS
# ===============================================================================

class FichaClinicaRepository:
    """
    Repositorio para gestionar operaciones CRUD de FichaClinica
    """
    
    def __init__(self, session: Session):
        self.session = session
    
    def crear_ficha(self, datos_ficha: Dict[str, Any]) -> FichaClinica:
        """
        Crea una nueva ficha clínica
        """
        try:
            ficha = FichaClinica(**datos_ficha)
            self.session.add(ficha)
            self.session.commit()
            self.session.refresh(ficha)
            
            logger.info(f"Ficha clínica creada: ID {ficha.id}")
            return ficha
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error al crear ficha clínica: {str(e)}")
            raise
    
    def obtener_por_id(self, ficha_id: int) -> Optional[FichaClinica]:
        """
        Obtiene una ficha clínica por ID con paciente y examen
        """
        return self.session.query(FichaClinica)\
            .options(
                joinedload(FichaClinica.paciente),
                joinedload(FichaClinica.examen_oftalmologico)
            )\
            .filter(FichaClinica.id == ficha_id)\
            .first()
    
    def obtener_fichas_paciente(self, paciente_id: int) -> List[FichaClinica]:
        """
        Obtiene todas las fichas clínicas de un paciente
        """
        return self.session.query(FichaClinica)\
            .filter(FichaClinica.paciente_id == paciente_id)\
            .order_by(desc(FichaClinica.fecha_consulta))\
            .all()
    
    def obtener_ultima_ficha_paciente(self, paciente_id: int) -> Optional[FichaClinica]:
        """
        Obtiene la última ficha clínica de un paciente
        """
        return self.session.query(FichaClinica)\
            .filter(FichaClinica.paciente_id == paciente_id)\
            .order_by(desc(FichaClinica.fecha_consulta))\
            .first()
    
    def obtener_fichas_fecha(self, fecha_inicio: date, fecha_fin: date) -> List[FichaClinica]:
        """
        Obtiene fichas clínicas en un rango de fechas
        """
        return self.session.query(FichaClinica)\
            .options(joinedload(FichaClinica.paciente))\
            .filter(
                and_(
                    func.date(FichaClinica.fecha_consulta) >= fecha_inicio,
                    func.date(FichaClinica.fecha_consulta) <= fecha_fin
                )
            )\
            .order_by(desc(FichaClinica.fecha_consulta))\
            .all()
    
    def actualizar_ficha(self, ficha_id: int, datos_actualizados: Dict[str, Any]) -> Optional[FichaClinica]:
        """
        Actualiza una ficha clínica
        """
        try:
            ficha = self.obtener_por_id(ficha_id)
            if not ficha:
                return None
            
            for key, value in datos_actualizados.items():
                if hasattr(ficha, key):
                    setattr(ficha, key, value)
            
            self.session.commit()
            logger.info(f"Ficha clínica actualizada: ID {ficha.id}")
            return ficha
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error al actualizar ficha clínica: {str(e)}")
            raise

# ===============================================================================
# REPOSITORIO EXÁMENES OFTALMOLÓGICOS
# ===============================================================================

class ExamenOftalmologicoRepository:
    """
    Repositorio para gestionar operaciones CRUD de ExamenOftalmologicoCompleto
    """
    
    def __init__(self, session: Session):
        self.session = session
    
    def crear_examen(self, datos_examen: Dict[str, Any]) -> ExamenOftalmologicoCompleto:
        """
        Crea un nuevo examen oftalmológico
        """
        try:
            examen = ExamenOftalmologicoCompleto(**datos_examen)
            self.session.add(examen)
            self.session.commit()
            self.session.refresh(examen)
            
            logger.info(f"Examen oftalmológico creado: ID {examen.id}")
            return examen
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error al crear examen oftalmológico: {str(e)}")
            raise
    
    def obtener_por_ficha(self, ficha_clinica_id: int) -> Optional[ExamenOftalmologicoCompleto]:
        """
        Obtiene el examen oftalmológico de una ficha clínica
        """
        return self.session.query(ExamenOftalmologicoCompleto)\
            .filter(ExamenOftalmologicoCompleto.ficha_clinica_id == ficha_clinica_id)\
            .first()
    
    def actualizar_examen(self, ficha_clinica_id: int, datos_actualizados: Dict[str, Any]) -> Optional[ExamenOftalmologicoCompleto]:
        """
        Actualiza o crea un examen oftalmológico
        """
        try:
            examen = self.obtener_por_ficha(ficha_clinica_id)
            
            if examen:
                # Actualizar examen existente
                for key, value in datos_actualizados.items():
                    if hasattr(examen, key):
                        setattr(examen, key, value)
            else:
                # Crear nuevo examen
                datos_actualizados['ficha_clinica_id'] = ficha_clinica_id
                examen = ExamenOftalmologicoCompleto(**datos_actualizados)
                self.session.add(examen)
            
            self.session.commit()
            self.session.refresh(examen)
            
            logger.info(f"Examen oftalmológico actualizado: ficha {ficha_clinica_id}")
            return examen
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error al actualizar examen oftalmológico: {str(e)}")
            raise
    
    def obtener_estadisticas_examenes(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de exámenes realizados
        """
        total_examenes = self.session.query(ExamenOftalmologicoCompleto).count()
        
        examenes_mes_actual = self.session.query(ExamenOftalmologicoCompleto)\
            .filter(extract('month', ExamenOftalmologicoCompleto.fecha_creacion) == datetime.now().month)\
            .count()
        
        return {
            'total_examenes': total_examenes,
            'examenes_mes_actual': examenes_mes_actual
        }
        
        """