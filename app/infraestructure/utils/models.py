# Importar todos los modelos para que SQLAlchemy los registre
from app.domain.models.user import User
from app.domain.models.products import Product
from app.domain.models.sale import Sale
from app.domain.models.cliente import Cliente
from app.domain.models.rol import Rol

# Modelos del módulo oftalmológico
from app.domain.models.paciente import Paciente
from app.domain.models.consulta_medica import ConsultaMedica
from app.domain.models.examen_basico import ExamenBasico
from app.domain.models.biomicroscopia import Biomicroscopia
from app.domain.models.oftalmoscopia import Oftalmoscopia
from app.domain.models.diagnostico import Diagnostico
from app.domain.models.receta_oftalmologica import RecetaOftalmologica

# Esto asegura que todos los modelos estén disponibles
__all__ = [
    'User', 'Product', 'Sale', 'Cliente', 'Rol',
    'Paciente', 'ConsultaMedica', 'ExamenBasico', 'Biomicroscopia', 
    'Oftalmoscopia', 'Diagnostico', 'RecetaOftalmologica'
] 