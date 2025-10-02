# ===============================================================================
# SERVICIOS - FICHA CLÍNICA DIGITAL
# Sistema: Oftalmetryc - Lógica de Negocio Fichas Clínicas
# Autor: Orlando Rodriguez
# Fecha: 2 de octubre de 2025
# ===============================================================================

from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, date
import logging
from sqlalchemy.orm import Session

from app.infraestructure.repositories.ficha_clinica_repository import (
    PacienteV2Repository, 
    FichaClinicaRepository, 
    ExamenOftalmologicoRepository
)
from app.domain.models.ficha_clinica_models import PacienteV2, FichaClinica, ExamenOftalmologicoCompleto

logger = logging.getLogger(__name__)

# ===============================================================================
# SERVICIO PRINCIPAL - FICHA CLÍNICA
# ===============================================================================

class FichaClinicaService:
    """
    Servicio principal para gestionar el flujo completo de fichas clínicas
    """
    
    def __init__(self, session: Session):
        self.session = session
        self.paciente_repo = PacienteV2Repository(session)
        self.ficha_repo = FichaClinicaRepository(session)
        self.examen_repo = ExamenOftalmologicoRepository(session)
    
    # =========================================================================
    # GESTIÓN DE PACIENTES
    # =========================================================================
    
    def buscar_o_crear_paciente(self, ci: str, datos_paciente: Dict[str, Any] = None) -> Tuple[PacienteV2, bool]:
        """
        Busca un paciente por CI, si no existe lo crea
        Returns: (paciente, es_nuevo)
        """
        try:
            # Buscar paciente existente
            paciente = self.paciente_repo.obtener_por_ci(ci)
            
            if paciente:
                logger.info(f"Paciente encontrado: {ci}")
                return paciente, False
            
            # Crear nuevo paciente si no existe
            if not datos_paciente:
                raise ValueError("Se requieren datos del paciente para crear uno nuevo")
            
            datos_paciente['ci'] = ci
            paciente = self.paciente_repo.crear_paciente(datos_paciente)
            logger.info(f"Nuevo paciente creado: {ci}")
            return paciente, True
            
        except Exception as e:
            logger.error(f"Error en buscar_o_crear_paciente: {str(e)}")
            raise
    
    def buscar_pacientes_avanzado(self, termino: str) -> List[Dict[str, Any]]:
        """
        Búsqueda avanzada de pacientes con información adicional
        """
        try:
            pacientes = self.paciente_repo.buscar_pacientes(termino)
            
            resultado = []
            for paciente in pacientes:
                ultima_consulta = self.ficha_repo.obtener_ultima_ficha_paciente(paciente.id)
                
                resultado.append({
                    'paciente': paciente,
                    'ultima_consulta': ultima_consulta.fecha_consulta if ultima_consulta else None,
                    'total_consultas': len(paciente.fichas_clinicas)
                })
            
            return resultado
            
        except Exception as e:
            logger.error(f"Error en buscar_pacientes_avanzado: {str(e)}")
            raise
    
    def obtener_perfil_completo_paciente(self, paciente_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene el perfil completo del paciente con estadísticas
        """
        try:
            paciente = self.paciente_repo.obtener_por_id(paciente_id)
            if not paciente:
                return None
            
            fichas = self.ficha_repo.obtener_fichas_paciente(paciente_id)
            
            # Calcular estadísticas
            total_consultas = len(fichas)
            ultima_consulta = fichas[0] if fichas else None
            
            # Diagnósticos más frecuentes
            diagnosticos = {}
            for ficha in fichas:
                if ficha.diagnostico_general:
                    diag = ficha.diagnostico_general.strip().lower()
                    diagnosticos[diag] = diagnosticos.get(diag, 0) + 1
            
            diagnostico_frecuente = max(diagnosticos, key=diagnosticos.get) if diagnosticos else None
            
            return {
                'paciente': paciente,
                'estadisticas': {
                    'total_consultas': total_consultas,
                    'ultima_consulta': ultima_consulta,
                    'diagnostico_frecuente': diagnostico_frecuente,
                    'usa_lentes': ultima_consulta.usa_lentes if ultima_consulta else False
                },
                'fichas_recientes': fichas[:5]  # Últimas 5 fichas
            }
            
        except Exception as e:
            logger.error(f"Error en obtener_perfil_completo_paciente: {str(e)}")
            raise
    
    # =========================================================================
    # GESTIÓN DE FICHAS CLÍNICAS
    # =========================================================================
    
    def crear_ficha_completa(self, paciente_id: int, datos_ficha: Dict[str, Any], 
                           datos_examen: Dict[str, Any] = None) -> FichaClinica:
        """
        Crea una ficha clínica completa con examen oftalmológico
        """
        try:
            # Verificar que el paciente existe
            paciente = self.paciente_repo.obtener_por_id(paciente_id)
            if not paciente:
                raise ValueError(f"Paciente con ID {paciente_id} no encontrado")
            
            # Crear ficha clínica
            datos_ficha['paciente_id'] = paciente_id
            ficha = self.ficha_repo.crear_ficha(datos_ficha)
            
            # Crear examen oftalmológico si se proporcionan datos
            if datos_examen:
                datos_examen['ficha_clinica_id'] = ficha.id
                self.examen_repo.crear_examen(datos_examen)
            
            logger.info(f"Ficha clínica completa creada: ID {ficha.id} para paciente {paciente_id}")
            return ficha
            
        except Exception as e:
            logger.error(f"Error en crear_ficha_completa: {str(e)}")
            raise
    
    def actualizar_ficha_completa(self, ficha_id: int, datos_ficha: Dict[str, Any] = None,
                                datos_examen: Dict[str, Any] = None) -> Optional[FichaClinica]:
        """
        Actualiza una ficha clínica y su examen oftalmológico
        """
        try:
            ficha = None
            
            # Actualizar datos de la ficha
            if datos_ficha:
                ficha = self.ficha_repo.actualizar_ficha(ficha_id, datos_ficha)
                if not ficha:
                    raise ValueError(f"Ficha con ID {ficha_id} no encontrada")
            
            # Actualizar examen oftalmológico
            if datos_examen:
                self.examen_repo.actualizar_examen(ficha_id, datos_examen)
            
            # Obtener ficha actualizada si no se obtuvo antes
            if not ficha:
                ficha = self.ficha_repo.obtener_por_id(ficha_id)
            
            logger.info(f"Ficha clínica completa actualizada: ID {ficha_id}")
            return ficha
            
        except Exception as e:
            logger.error(f"Error en actualizar_ficha_completa: {str(e)}")
            raise
    
    def obtener_ficha_completa(self, ficha_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene una ficha clínica completa con todos sus datos
        """
        try:
            ficha = self.ficha_repo.obtener_por_id(ficha_id)
            if not ficha:
                return None
            
            examen = self.examen_repo.obtener_por_ficha(ficha_id)
            
            return {
                'ficha': ficha,
                'paciente': ficha.paciente,
                'examen': examen
            }
            
        except Exception as e:
            logger.error(f"Error en obtener_ficha_completa: {str(e)}")
            raise
    
    def obtener_historial_paciente(self, paciente_id: int) -> Dict[str, Any]:
        """
        Obtiene el historial completo de consultas de un paciente
        """
        try:
            paciente = self.paciente_repo.obtener_por_id(paciente_id)
            if not paciente:
                raise ValueError(f"Paciente con ID {paciente_id} no encontrado")
            
            fichas = self.ficha_repo.obtener_fichas_paciente(paciente_id)
            
            # Organizar fichas por año
            fichas_por_año = {}
            for ficha in fichas:
                año = ficha.fecha_consulta.year
                if año not in fichas_por_año:
                    fichas_por_año[año] = []
                fichas_por_año[año].append(ficha)
            
            return {
                'paciente': paciente,
                'total_consultas': len(fichas),
                'fichas_por_año': fichas_por_año,
                'ultima_consulta': fichas[0] if fichas else None
            }
            
        except Exception as e:
            logger.error(f"Error en obtener_historial_paciente: {str(e)}")
            raise
    
    # =========================================================================
    # VALIDACIONES Y UTILIDADES
    # =========================================================================
    
    def validar_cedula_ecuador(self, ci: str) -> Tuple[bool, str]:
        """
        Valida cédula de identidad ecuatoriana
        """
        try:
            if not ci or len(ci) != 10:
                return False, "La cédula debe tener 10 dígitos"
            
            if not ci.isdigit():
                return False, "La cédula debe contener solo números"
            
            # Validar provincia (primeros 2 dígitos)
            provincia = int(ci[:2])
            if provincia < 1 or provincia > 24:
                return False, "Código de provincia inválido"
            
            # Algoritmo de validación del último dígito
            coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
            suma = 0
            
            for i in range(9):
                producto = int(ci[i]) * coeficientes[i]
                if producto >= 10:
                    producto = producto - 9
                suma += producto
            
            digito_verificador = (10 - (suma % 10)) % 10
            
            if digito_verificador != int(ci[9]):
                return False, "Cédula inválida según algoritmo de verificación"
            
            return True, "Cédula válida"
            
        except Exception as e:
            return False, f"Error al validar cédula: {str(e)}"
    
    def generar_resumen_ficha(self, ficha_id: int) -> Optional[Dict[str, Any]]:
        """
        Genera un resumen de la ficha para impresión o visualización rápida
        """
        try:
            datos_completos = self.obtener_ficha_completa(ficha_id)
            if not datos_completos:
                return None
            
            ficha = datos_completos['ficha']
            paciente = datos_completos['paciente']
            examen = datos_completos['examen']
            
            # Extraer información clave del examen
            info_clave = {}
            if examen:
                info_clave = {
                    'agudeza_visual': {
                        'od': examen.av_distancia_od,
                        'oi': examen.av_distancia_oi
                    },
                    'rx_final': {
                        'od': f"{examen.rx_esf_od or ''} {examen.rx_cyl_od or ''} x {examen.rx_eje_od or ''}".strip(),
                        'oi': f"{examen.rx_esf_oi or ''} {examen.rx_cyl_oi or ''} x {examen.rx_eje_oi or ''}".strip()
                    },
                    'presion_intraocular': {
                        'od': examen.presion_intraocular_od,
                        'oi': examen.presion_intraocular_oi
                    }
                }
            
            return {
                'paciente': {
                    'nombre_completo': paciente.nombre_completo,
                    'ci': paciente.ci,
                    'edad': paciente.edad,
                    'telefono': paciente.telefono
                },
                'consulta': {
                    'fecha': ficha.fecha_consulta,
                    'motivo': ficha.motivo_consulta,
                    'diagnostico': ficha.diagnostico_general,
                    'tratamiento': ficha.tratamiento_general
                },
                'examen_clave': info_clave,
                'responsable': ficha.firma_responsable
            }
            
        except Exception as e:
            logger.error(f"Error en generar_resumen_ficha: {str(e)}")
            raise
    
    # =========================================================================
    # ESTADÍSTICAS Y REPORTES
    # =========================================================================
    
    def obtener_estadisticas_generales(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas generales del sistema
        """
        try:
            # Estadísticas de pacientes
            total_pacientes = self.session.query(PacienteV2)\
                .filter(PacienteV2.estado == 'Activo').count()
            
            # Estadísticas de fichas
            total_fichas = self.session.query(FichaClinica).count()
            
            fichas_mes = self.session.query(FichaClinica)\
                .filter(
                    FichaClinica.fecha_consulta >= datetime.now().replace(day=1)
                ).count()
            
            # Estadísticas de exámenes
            stats_examenes = self.examen_repo.obtener_estadisticas_examenes()
            
            return {
                'pacientes': {
                    'total_activos': total_pacientes
                },
                'fichas': {
                    'total': total_fichas,
                    'mes_actual': fichas_mes
                },
                'examenes': stats_examenes
            }
            
        except Exception as e:
            logger.error(f"Error en obtener_estadisticas_generales: {str(e)}")
            raise