# Importar todos los modelos para SQLAlchemy
from .user import User
from .rol import Rol
from .cliente import Cliente
from .products import Product
from .sale import Sale
from .paciente import PacienteMedico
from .consulta_medica import FichaClinica
from .biomicroscopia import Biomicroscopia
from .examenes_medicos import FondoOjo, PresionIntraocular, CampoVisual, DiagnosticoMedico, Tratamiento

__all__ = [
    'User',
    'Rol', 
    'Cliente',
    'Product',
    'Sale',
    'PacienteMedico',
    'FichaClinica',
    'Biomicroscopia',
    'FondoOjo',
    'PresionIntraocular',
    'CampoVisual',
    'DiagnosticoMedico',
    'Tratamiento'
]