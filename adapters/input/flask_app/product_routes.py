from flask_restx import Namespace, Resource, fields
from app.domain.use_cases.product_use_cases import ProductUseCases
from app.infraestructure.utils.exceptions import ProductCreationError

# Crear namespace para productos
ns_products = Namespace('Productos', description='Operaciones de API relacionadas con productos')

# Se crea UNA SOLA instancia del servicio para todo el namespace.
product_use_cases = ProductUseCases()

# Modelo para documentación Swagger
product_model = ns_products.model('Producto', {
    'producto_id': fields.Integer(readonly=True),
    'nombre': fields.String(required=True, description='Nombre del producto'),
    'descripcion': fields.String(required=True, description='Descripción del producto'),
    'precio_unitario': fields.Float(required=True, description='Precio unitario'),
    'stock': fields.Integer(required=True, description='Stock disponible'),
    'categoria': fields.String,
    'marca': fields.String,
    'sku': fields.String,
    'estado': fields.Boolean,
})

# Parser para entrada POST/PUT
product_parser = ns_products.parser()
product_parser.add_argument('nombre', type=str, required=True, location='json')
product_parser.add_argument('descripcion', type=str, required=True, location='json')
product_parser.add_argument('precio_unitario', type=float, required=True, location='json')
product_parser.add_argument('stock', type=int, required=True, location='json')
product_parser.add_argument('categoria', type=str, location='json')
product_parser.add_argument('marca', type=str, location='json')
product_parser.add_argument('sku', type=str, location='json')

@ns_products.route('/')
class ProductList(Resource):
    @ns_products.marshal_list_with(product_model)
    def get(self):
        """Listar todos los productos activos"""
        return product_use_cases.list_products()

    @ns_products.expect(product_parser)
    @ns_products.marshal_with(product_model, code=201)
    def post(self):
        """Crear un nuevo producto"""
        args = product_parser.parse_args()
        try:
            product = product_use_cases.create_product(args)
            return product, 201
        except (ValueError, ProductCreationError) as e:
            ns_products.abort(400, str(e))
        except Exception as e:
            ns_products.abort(500, "Error interno del servidor al crear el producto.")

@ns_products.route('/<int:product_id>')
@ns_products.param('product_id', 'ID del producto')
class ProductResource(Resource):
    @ns_products.marshal_with(product_model)
    def get(self, product_id):
        """Obtener un producto por ID"""
        product = product_use_cases.get_product(product_id)
        if product:
            return product
        ns_products.abort(404, f"Producto con ID {product_id} no encontrado.")

    @ns_products.expect(product_parser)
    @ns_products.marshal_with(product_model)
    def put(self, product_id):
        """Actualizar un producto existente"""
        args = product_parser.parse_args()
        try:
            product = product_use_cases.update_product(product_id, args)
            if product:
                return product
            ns_products.abort(404, f"Producto con ID {product_id} no encontrado para actualizar.")
        except ValueError as e:
            ns_products.abort(400, str(e))
        except Exception as e:
            ns_products.abort(500, "Error interno del servidor al actualizar el producto.")

    @ns_products.response(204, 'Producto eliminado exitosamente')
    def delete(self, product_id):
        """Eliminar (desactivar) un producto"""
        result = product_use_cases.delete_product(product_id)
        if result is not None:
            return '', 204
        ns_products.abort(404, f"Producto con ID {product_id} no encontrado para eliminar.")
