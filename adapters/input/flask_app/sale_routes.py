from flask_restx import Namespace, Resource, fields, reqparse
from app.domain.use_cases.services.sale_service import SaleService
from flask import request

ns_sales = Namespace('Ventas', description='Operaciones relacionadas con ventas')
sale_service = SaleService()

sale_model = ns_sales.model('Sale', {
    'venta_id': fields.Integer(readonly=True),
    'producto_id': fields.Integer,
    'usuario_id': fields.Integer,
    'cantidad': fields.Integer,
    'total': fields.Float,
    'cliente': fields.String,
    'fecha': fields.DateTime
})

sale_parser = ns_sales.parser()
sale_parser.add_argument('producto_id', type=int, required=True)
sale_parser.add_argument('usuario_id', type=int, required=True)
sale_parser.add_argument('cantidad', type=int, required=True)
sale_parser.add_argument('total', type=float, required=True)
sale_parser.add_argument('cliente', type=str)

@ns_sales.route('/')
class SaleList(Resource):
    @ns_sales.marshal_list_with(sale_model)
    def get(self):
        return sale_service.get_all_sales()

    @ns_sales.expect(sale_parser)
    @ns_sales.marshal_with(sale_model, code=201)
    def post(self):
        args = sale_parser.parse_args()
        sale = sale_service.register_sale(
            producto_id=args['producto_id'],
            usuario_id=args['usuario_id'],
            cantidad=args['cantidad'],
            total=args['total'],
            cliente=args.get('cliente')
        )
        if sale:
            return sale, 201
        return {'message': 'Venta no registrada (stock insuficiente o error)'}, 400

@ns_sales.route('/<int:venta_id>')
@ns_sales.param('venta_id', 'ID de la venta')
class SaleResource(Resource):
    @ns_sales.marshal_with(sale_model)
    def get(self, venta_id):
        sale = sale_service.get_sale(venta_id)
        if sale:
            return sale, 200
        return {'message': 'Venta no encontrada'}, 404

    def delete(self, venta_id):
        if sale_service.delete_sale(venta_id):
            return {'message': 'Venta eliminada'}, 200
        return {'message': 'Venta no encontrada'}, 404 