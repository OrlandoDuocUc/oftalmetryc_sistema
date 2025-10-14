# app/domain/models/__init__.py
# Importa SIEMPRE los modelos base (seguros)
from .user import User
from .rol import Rol
from .cliente import Cliente
from .products import Product
from .sale import Sale
from .paciente import PacienteMedico
from .consulta_medica import FichaClinica

# Importaciones MÉDICAS opcionales (no romper el arranque si fallan)
try:
    from .examenes_medicos import (
        FondoOjo,
        PresionIntraocular,
        CampoVisual,
        DiagnosticoMedico,
        Tratamiento,
    )
except Exception:
    FondoOjo = None
    PresionIntraocular = None
    CampoVisual = None
    DiagnosticoMedico = None
    Tratamiento = None

__all__ = [
    "User",
    "Rol",
    "Cliente",
    "Product",
    "Sale",
    "PacienteMedico",
    "FichaClinica",
    "FondoOjo",
    "PresionIntraocular",
    "CampoVisual",
    "DiagnosticoMedico",
    "Tratamiento",
]
