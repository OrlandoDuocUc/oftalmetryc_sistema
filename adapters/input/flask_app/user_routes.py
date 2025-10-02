from flask_restx import Namespace, Resource, fields, reqparse
from adapters.output.repositories.user_repository import UserRepository  # Legacy, no usar
from app.domain.use_cases.services.user_service import UserService
from flask import request

# Crear namespace
ns_users = Namespace('Usuarios', description='Operaciones relacionadas con usuarios')

# Inyección de dependencias
user_service = UserService()

# Modelo para documentación Swagger
user_model = ns_users.model('User', {
    'id': fields.Integer(readonly=True),
    'nombre': fields.String,
    'usuario': fields.String,
    'email': fields.String,
    'rol': fields.String,
    'estado': fields.String
})

register_parser = ns_users.parser()
register_parser.add_argument('nombre', type=str, required=True)
register_parser.add_argument('usuario', type=str, required=True)
register_parser.add_argument('email', type=str, required=True)
register_parser.add_argument('password', type=str, required=True)
register_parser.add_argument('rol', type=str, default='vendedor')
register_parser.add_argument('ap_pat', type=str, required=True)
register_parser.add_argument('ap_mat', type=str, required=True)

login_parser = ns_users.parser()
login_parser.add_argument('usuario', type=str, required=True)
login_parser.add_argument('password', type=str, required=True)

@ns_users.route('/register')
class UserRegister(Resource):
    @ns_users.expect(register_parser)
    @ns_users.marshal_with(user_model, code=201)
    def post(self):
        args = register_parser.parse_args()
        user = user_service.register_user(
            nombre=args['nombre'], ap_pat=args['ap_pat'], ap_mat=args['ap_mat'], usuario=args['usuario'], email=args['email'], password=args['password'], rol=args['rol'])
        return user, 201

@ns_users.route('/login')
class UserLogin(Resource):
    @ns_users.expect(login_parser)
    def post(self):
        args = login_parser.parse_args()
        user = user_service.authenticate(args['usuario'], args['password'])
        if user:
            return {'message': 'Login exitoso', 'user_id': user.id, 'rol': user.rol}, 200
        return {'message': 'Credenciales inválidas'}, 401

@ns_users.route('/')
class UserList(Resource):
    @ns_users.marshal_list_with(user_model)
    def get(self):
        return user_service.get_all_users()

@ns_users.route('/<int:user_id>')
@ns_users.param('user_id', 'ID del usuario')
class UserResource(Resource):
    @ns_users.marshal_with(user_model)
    def get(self, user_id):
        user = user_service.get_user(user_id)
        if user:
            return user, 200
        return {'message': 'Usuario no encontrado'}, 404

    def delete(self, user_id):
        if user_service.delete_user(user_id):
            return {'message': 'Usuario eliminado'}, 200
        return {'message': 'Usuario no encontrado'}, 404

__all__ = ['ns_users']