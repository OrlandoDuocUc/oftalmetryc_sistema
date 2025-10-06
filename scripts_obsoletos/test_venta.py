#!/usr/bin/env python3
"""
Script de prueba para verificar el registro de ventas
"""
from app.infraestructure.utils.db import SessionLocal
from app.domain.models.products import Product
from app.domain.models.sale import Sale
from app.domain.models.user import User
from app.domain.use_cases.services.sale_service import SaleService
from app.domain.use_cases.product_use_cases import ProductUseCases
from app.infraestructure.repositories.sql_product_repository import SQLProductRepository

def test_venta():
    print("🧪 Probando registro de ventas...")
    
    # Crear servicios
    sale_service = SaleService()
    db_session = SessionLocal()
    product_repo = SQLProductRepository(db_session)
    product_service = ProductUseCases(product_repo)
    
    try:
        # 1. Verificar productos existentes
        productos = product_service.list_products()
        print(f"📦 Productos encontrados: {len(productos)}")
        
        if not productos:
            print("❌ No hay productos para probar ventas")
            return False
        
        # Mostrar primer producto
        primer_producto = productos[0]
        print(f"🔍 Primer producto: {primer_producto.nombre} - Stock: {primer_producto.stock} - Precio: ${primer_producto.precio_unitario}")
        
        # 2. Verificar usuarios existentes
        usuarios = db_session.query(User).all()
        print(f"👥 Usuarios encontrados: {len(usuarios)}")
        
        if not usuarios:
            print("❌ No hay usuarios para probar ventas")
            return False
        
        primer_usuario = usuarios[0]
        print(f"🔍 Primer usuario: {primer_usuario.nombre} (ID: {primer_usuario.usuario_id})")
        
        # 3. Probar registro de venta
        print("\n💰 Registrando venta de prueba...")
        resultado = sale_service.register_sale(
            producto_id=primer_producto.producto_id,
            usuario_id=primer_usuario.usuario_id,
            cantidad=1,
            total=primer_producto.precio_unitario,
            cliente_id=None
        )
        
        if resultado:
            print("✅ Venta registrada exitosamente!")
            print(f"📊 ID de venta: {resultado.venta_id}")
            print(f"📦 Cantidad: {resultado.cantidad}")
            print(f"💰 Total: ${resultado.total}")
            print(f"📅 Fecha: {resultado.fecha}")
            
            # 4. Verificar que el stock se actualizó
            producto_actualizado = product_service.get_product(primer_producto.producto_id)
            if producto_actualizado:
                print(f"📦 Stock actualizado: {producto_actualizado.stock} (era {primer_producto.stock})")
            else:
                print("❌ No se pudo obtener el producto actualizado")
            
            # 5. Verificar historial
            ventas = sale_service.get_all_sales_with_details()
            print(f"📋 Total de ventas en historial: {len(ventas)}")
            
            if ventas:
                ultima_venta = ventas[0]
                print(f"📋 Última venta: {ultima_venta['producto_nombre']} - ${ultima_venta['total']}")
            
            return True
        else:
            print("❌ Error al registrar venta")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        return False
    finally:
        db_session.close()

if __name__ == "__main__":
    test_venta() 