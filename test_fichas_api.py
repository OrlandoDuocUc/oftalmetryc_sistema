#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para probar el endpoint de fichas clínicas
"""

import requests
import json

def test_fichas_clinicas_api():
    """Prueba el endpoint /api/fichas-clinicas"""
    print("🔍 PROBANDO ENDPOINT /api/fichas-clinicas")
    print("=" * 50)
    
    # URL del endpoint
    url = "http://127.0.0.1:5000/api/fichas-clinicas"
    
    try:
        # Realizar petición GET
        print(f"📡 Haciendo GET a: {url}")
        response = requests.get(url)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ Respuesta JSON válida:")
                print(json.dumps(data, indent=2, ensure_ascii=False))
                
                if 'data' in data:
                    fichas = data['data']
                    print(f"\n📈 Total fichas encontradas: {len(fichas)}")
                    
                    if fichas:
                        print("\n🔍 Primera ficha de ejemplo:")
                        print(json.dumps(fichas[0], indent=2, ensure_ascii=False))
                    else:
                        print("⚠️ No hay fichas clínicas en la respuesta")
                else:
                    print("⚠️ La respuesta no tiene el formato esperado (falta 'data')")
                    
            except json.JSONDecodeError as e:
                print(f"❌ Error decodificando JSON: {e}")
                print(f"📝 Respuesta cruda: {response.text}")
                
        elif response.status_code == 404:
            print("❌ Endpoint no encontrado (404)")
        elif response.status_code == 500:
            print("❌ Error interno del servidor (500)")
            print(f"📝 Respuesta: {response.text}")
        else:
            print(f"❌ Error inesperado: {response.status_code}")
            print(f"📝 Respuesta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión. ¿Está Flask corriendo en puerto 5000?")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_fichas_clinicas_api()