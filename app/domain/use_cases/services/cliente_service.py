from app.domain.models.cliente import Cliente
from app.infraestructure.repositories.sql_cliente_repository import SQLClienteRepository
from app.infraestructure.utils.db_session import get_db_session, close_db_session
from sqlalchemy.exc import SQLAlchemyError

class ClienteService:
    def __init__(self):
        pass

    def _get_repository(self):
        """Obtiene una sesión de base de datos y crea el repositorio"""
        db_session = get_db_session()
        cliente_repository = SQLClienteRepository(db_session)
        return db_session, cliente_repository

    def create_cliente(self, nombres, ap_pat, ap_mat=None, email=None, telefono=None, direccion=None):
        """Crea un nuevo cliente y devuelve su ID"""
        db_session, cliente_repository = self._get_repository()
        try:
            cliente = Cliente(
                nombres=nombres,
                ap_pat=ap_pat,
                ap_mat=ap_mat,
                email=email,
                telefono=telefono,
                direccion=direccion
            )
            saved_cliente = cliente_repository.save(cliente)
            if saved_cliente:
                # Devolver solo el ID del cliente para evitar problemas de sesión
                return saved_cliente.cliente_id
            return None
        finally:
            close_db_session(db_session)

    def get_cliente_by_name(self, nombres, ap_pat):
        """Busca un cliente por nombre y apellido paterno"""
        db_session, cliente_repository = self._get_repository()
        try:
            cliente = db_session.query(Cliente).filter(
                Cliente.nombres.ilike(f"%{nombres}%"),
                Cliente.ap_pat.ilike(f"%{ap_pat}%")
            ).first()
            if cliente:
                # Devolver solo el ID para evitar problemas de sesión
                return cliente.cliente_id
            return None
        finally:
            close_db_session(db_session)

    def get_cliente_by_id(self, cliente_id):
        """Obtiene un cliente por ID y devuelve sus datos como diccionario"""
        db_session, cliente_repository = self._get_repository()
        try:
            cliente = cliente_repository.get_by_id(cliente_id)
            if cliente:
                # Devolver datos como diccionario para evitar problemas de sesión
                return {
                    'cliente_id': cliente.cliente_id,
                    'nombres': cliente.nombres,
                    'ap_pat': cliente.ap_pat,
                    'ap_mat': cliente.ap_mat,
                    'email': cliente.email,
                    'telefono': cliente.telefono,
                    'direccion': cliente.direccion,
                    'fecha_creacion': cliente.fecha_creacion,
                    'estado': cliente.estado
                }
            return None
        finally:
            close_db_session(db_session)

    def get_all_clientes(self):
        """Obtiene todos los clientes como lista de diccionarios"""
        db_session, cliente_repository = self._get_repository()
        try:
            clientes = cliente_repository.get_all()
            # Convertir a lista de diccionarios para evitar problemas de sesión
            return [
                {
                    'cliente_id': cliente.cliente_id,
                    'nombres': cliente.nombres,
                    'ap_pat': cliente.ap_pat,
                    'ap_mat': cliente.ap_mat,
                    'email': cliente.email,
                    'telefono': cliente.telefono,
                    'direccion': cliente.direccion,
                    'fecha_creacion': cliente.fecha_creacion,
                    'estado': cliente.estado
                }
                for cliente in clientes
            ]
        finally:
            close_db_session(db_session) 