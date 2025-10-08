from flask_restx import Namespace, Resource, fields
from app.domain.use_cases.services.sale_service import SaleService

ns_sales = Namespace('Ventas', description='Operaciones de API relacionadas con ventas')

# Se crea UNA SOLA instancia del servicio.
sale_service = SaleService()

# Modelo para documentación Swagger
sale_model = ns_sales.model('Sale', {
    'venta_id': fields.Integer(readonly=True),
    'producto_id': fields.Integer(required=True),
    'usuario_id': fields.Integer(required=True),
    'cantidad': fields.Integer(required=True),
    'total': fields.Float(required=True),
    'cliente_id': fields.Integer,
    'fecha_venta': fields.DateTime(readonly=True)
})

# Parser para la entrada POST
sale_parser = ns_sales.parser()
sale_parser.add_argument('producto_id', type=int, required=True, location='json')
sale_parser.add_argument('usuario_id', type=int, required=True, location='json')
sale_parser.add_argument('cantidad', type=int, required=True, location='json')
sale_parser.add_argument('total', type=float, required=True, location='json')
sale_parser.add_argument('cliente_id', type=int, location='json')

@ns_sales.route('/')
class SaleList(Resource):
    @ns_sales.marshal_list_with(sale_model)
    def get(self):
        """Listar todas las ventas con sus detalles"""
        return sale_service.get_all_sales_with_details()

    @ns_sales.expect(sale_parser)
    def post(self):
        """Registrar una nueva venta (API)"""
        args = sale_parser.parse_args()
        try:
            # Esta ruta ahora es para una sola venta, no el carrito completo
            venta_id = sale_service.register_sale_from_cart([args], args['usuario_id'], {})
            return {'message': 'Venta registrada exitosamente', 'venta_id': venta_id}, 201
        except ValueError as e:
            ns_sales.abort(400, str(e))
        except Exception as e:
            ns_sales.abort(500, "Error interno al registrar la venta.")

@ns_sales.route('/<int:venta_id>')
@ns_sales.param('venta_id', 'ID de la venta')
class SaleResource(Resource):
    @ns_sales.marshal_with(sale_model)
    def get(self, venta_id):
        """Obtener una venta específica por su ID con todos los detalles"""
        sale = sale_service.get_sale_details_for_receipt(venta_id)
        if sale:
            return sale
        ns_sales.abort(404, f"Venta con ID {venta_id} no encontrada.")

