from flask_restx import Namespace, Resource, fields, reqparse
from app.domain.use_cases.product_use_cases import ProductUseCases
from app.infraestructure.repositories.sql_product_repository import SQLProductRepository
from app.infraestructure.utils.db import SessionLocal
from app.infraestructure.utils.exceptions import ProductCreationError

# Crear namespace para productos
ns_products = Namespace('Producto', description='Operaciones relacionadas con productos')

# Inyección de dependencias
db_session = SessionLocal()
product_repo = SQLProductRepository(db_session)
product_use_cases = ProductUseCases(product_repo)

# Modelo para documentación Swagger
product_model = ns_products.model('Producto', {
    'producto_id': fields.Integer(readonly=True),
    'nombre': fields.String(required=True, description='Nombre del producto'),
    'descripcion': fields.String(required=True, description='Descripción del producto'),
    'precio_unitario': fields.Float(required=True, description='Precio unitario del producto'),
    'stock': fields.Integer(description='Stock disponible'),
    'fecha_creacion': fields.DateTime(description='Fecha de creación del producto'),
    'estado': fields.String(description='Estado del producto (por defecto "A" para Activo)'),
})

# Parser para entrada POST/PUT
product_parser = ns_products.parser()
product_parser.add_argument('producto_id', type=int, help='ID del producto', location='json')
product_parser.add_argument('nombre', type=str, required=True, help='Nombre del producto', location='json')
product_parser.add_argument('descripcion', type=str, required=True, help='Descripción del producto', location='json')
product_parser.add_argument('precio_unitario', type=float, required=True, help='Precio unitario del producto', location='json')
product_parser.add_argument('stock', type=int, required=True, help='Stock disponible', location='json')
product_parser.add_argument('fecha_creacion', type=str, help='Fecha de creación del producto (Formato ISO)', location='json')
product_parser.add_argument('estado', type=str, help='Estado del producto (por defecto "A")', location='json')

# Definición de rutas y métodos
@ns_products.route('/')
class ProductList(Resource):
    @ns_products.marshal_list_with(product_model)
    @ns_products.response(200, 'Listado de productos obtenido correctamente')
    @ns_products.response(500, 'Error interno del servidor')
    def get(self):
        """Listar todos los productos"""
        products = product_use_cases.list_products()
        return products, 200

    @ns_products.expect(product_parser)
    @ns_products.marshal_with(product_model, code=201)
    @ns_products.response(201, 'Producto creado exitosamente')
    @ns_products.response(400, 'Solicitud inválida')
    @ns_products.response(409, 'Conflicto al crear el producto')
    @ns_products.response(500, 'Error interno del servidor')
    def post(self):
        """Crear un nuevo producto"""
        args = product_parser.parse_args()
        try:
            product = product_use_cases.create_product(args)
            return product, 201
        except ProductCreationError as e:
            return {'message': str(e)}, 409
        except Exception as e:
            return {'message': 'Error interno del servidor'}, 500

@ns_products.route('/<int:product_id>')
@ns_products.param('product_id', 'ID del producto')
class ProductResource(Resource):
    @ns_products.marshal_with(product_model)
    @ns_products.response(200, 'Producto obtenido exitosamente')
    @ns_products.response(404, 'Producto no encontrado')
    @ns_products.response(500, 'Error interno del servidor')
    def get(self, product_id):
        """Obtener un producto por ID"""
        product = product_use_cases.get_product(product_id)
        if product:
            return product, 200
        ns_products.abort(404, "Producto no encontrado")

    @ns_products.expect(product_parser)
    @ns_products.marshal_with(product_model)
    @ns_products.response(200, 'Producto actualizado exitosamente')
    @ns_products.response(400, 'Solicitud inválida')
    @ns_products.response(404, 'Producto no encontrado')
    @ns_products.response(500, 'Error interno del servidor')
    def put(self, product_id):
        """Actualizar un producto existente"""
        args = product_parser.parse_args()
        product = product_use_cases.update_product(product_id, args)
        if product:
            return product, 200
        ns_products.abort(404, "Producto no encontrado")

    @ns_products.response(200, 'Producto eliminado exitosamente')
    @ns_products.response(404, 'Producto no encontrado')
    @ns_products.response(500, 'Error interno del servidor')
    def delete(self, product_id):
        """Eliminar un producto"""
        result = product_use_cases.delete_product(product_id)
        if result:
            return {'message': 'Producto eliminado'}, 200
        ns_products.abort(404, "Producto no encontrado")

__all__ = ['ns_products']
