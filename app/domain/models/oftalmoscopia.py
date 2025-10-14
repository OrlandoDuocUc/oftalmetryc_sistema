# app/domain/models/oftalmoscopia.py
# --------------------------------------------------------------------
# Compatibilidad: re-exporta el modelo real 'FondoOjo' definido en
# app.domain.models.examenes_medicos, evitando un segundo mapeo a la
# misma tabla 'fondo_ojo'.
# --------------------------------------------------------------------

from app.domain.models.examenes_medicos import FondoOjo

__all__ = ["FondoOjo"]
